#!/usr/bin/env python

# Copyright (C) 2022 Ariel Ortiz

"""A compiler for the chiqui_forth programming language.

Translates a chiqui_forth source file into the corresponding WAT
and WASM code.

To run, at the terminal type:

    python chiqui_forth.py some_program.4th

If successful, the program produces two output files:

    some_program.wat   (WebAssembly text format)
    some_program.wasm  (WebAssembly binary format)
"""

from os.path import splitext
from sys import argv, stderr, exit
from wasmer import wat2wasm

WAT_SOURCE_BEGIN = ''';; chiqui_forth compiler WAT output

(module
  (import "forth" "emit" (func $emit (param i32)))
  (import "forth" "input" (func $input (result i32)))
  (import "forth" "print" (func $print (param i32)))
  (func (export "_start")'''

WAT_SOURCE_END = '''  )
)'''

OPERATION = {
    '*': ['i32.mul'],
    '+': ['i32.add'],
    '.': ['call $print'],
    'emit': ['call $emit'],
    'input': ['call $input'],
    'nl': [
        'i32.const 10',
        'call $emit'
    ],
}

INDENTATION = '    '

def check_args():
    """Verify that there is one command line argument; if not, display
    an error message and exit.
    """
    if len(argv) != 2:
        print('Please specify the name of the Forth source file.',
            file=stderr)
        exit(1)


def read_words(input_file_name):
    """Read the content from the input file and split it into
    space-delimited words.
    """
    try:
        with open(argv[1]) as source_file:
            source_text = source_file.read()
        return source_text.split()
    except FileNotFoundError:
        print(f'Oops! File not found: {input_file_name}', file=stderr)
        exit(1)


def remove_comments(words):
    """Remove all the words that constitute part of a comment."""
    commentless_words = []
    inside_comment = False
    for word in words:
        if inside_comment:
            if word == ')':
                inside_comment = False
        elif word == '(':
            inside_comment = True
        else:
            commentless_words.append(word)
    words[:] = commentless_words


def is_var_name(word):
    """Return true if word is a variable name, false otherwise."""
    return (word[0].isalpha()
            and word.isalnum()
            and word not in OPERATION)


def is_number(word):
    """Return true if word is a valid integer, false otherwise."""
    try:
        int(word)
        return True
    except ValueError:
        return False


def find_vars_used(words):
    """Find all the variables used in the program."""
    names = set()
    for word in words:
        name = word[:-1] if word[-1] == '!' else word
        if is_var_name(name):
            names.add(name)
    return names


def declare_vars(result, vars):
    """Append to result the WAT declarations of each variable
    contained in var.
    """
    for var in vars:
        result.append(INDENTATION + f'(local ${var} i32)')


def code_generation(result, words):
    """Translate every word from the source code into its equivalent
    WAT instructions and append them to result.
    """
    for word in words:
        if is_number(word):
            result.append(INDENTATION + f'i32.const {word}')
        elif word in OPERATION:
            for statement in OPERATION[word]:
                result.append(INDENTATION + statement)
        elif is_var_name(word):
            result.append(INDENTATION + f'local.get ${word}')
        elif word[-1] == '!' and is_var_name(word[:-1]):
            result.append(INDENTATION + f'local.set ${word[:-1]}')
        else:
            raise ValueError(f"'{word}' is not a valid word")


def create_wat_file(file_name, file_content):
    """Create a text file with the WAT code."""
    with open(file_name + '.wat', 'w') as file:
        file.write(file_content)


def create_wasm_file(file_name, file_content):
    """Create a binary file with the WASM code."""
    with open(file_name + '.wasm', 'wb') as file:
        file.write(wat2wasm(file_content))


def main():
    """Control all the steps carried out by the compiler."""
    check_args()
    full_source_name = argv[1]
    words = read_words(full_source_name)
    remove_comments(words)
    result = []
    result.append(WAT_SOURCE_BEGIN)
    declare_vars(result, find_vars_used(words))
    code_generation(result, words)
    result.append(WAT_SOURCE_END)
    file_content = '\n'.join(result)
    file_name, _ = splitext(full_source_name)
    create_wat_file(file_name, file_content)
    create_wasm_file(file_name, file_content)


if __name__ == '__main__':
    main()
