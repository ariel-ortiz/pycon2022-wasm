#!/usr/bin/env python

# Copyright (C) 2022 Ariel Ortiz

"""WASM code execution script.

To run, at the terminal type:

    python execute.py some_program.wasm
"""

from sys import argv, stdin, stderr, exit
from wasmer import engine, Module, Store, Instance, ImportObject, Function
from wasmer_compiler_cranelift import Compiler


def make_import_object(store):
    """Create an import object that registers the Python functions
    that will be callable from the WASM module.
    """

    #----------------------------------------------------------------
    # Functions to be imported from the WASM module.
    # Note that we need to use type annotations.

    def _emit(x: int):
        print(chr(x), end='')

    def _input() -> int:
        try:
            return int(input())
        except ValueError:
            return 0

    def _print(x: int):
        print(x, end=' ')

    #----------------------------------------------------------------

    import_object = ImportObject()

    import_object.register(
        "forth",
        {
            "emit": Function(store, _emit),
            "input": Function(store, _input),
            "print": Function(store, _print)
        }
    )

    return import_object


def create_instance(file_name):
    """Use wasmer API to take care of all the details required to
    instantiate a module contained in a WASM file.
    """
    store = Store(engine.JIT(Compiler))
    with open(file_name, 'rb') as file:
        return Instance(Module(store, file.read()),
                        make_import_object(store))


def check_args():
    """Verify that there is one command line argument; if not, display
    an error message and exit.
    """
    if len(argv) != 2:
        print('Please specify the name of the WASM binary file.',
            file=stderr)
        exit(1)


def main():
    """Control the steps to execute a WASM module."""
    check_args()
    instance = create_instance(argv[1])
    instance.exports._start() # Run the exported _start function


if __name__ == '__main__':
    main()
