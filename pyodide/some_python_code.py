# Copyright (C) 2022 Ariel Ortiz

"""Some Python code to test Pyodide."""

from datetime import datetime
from random import choice
from sys import version

ONELINERS = [
    'A data scientist is a person who is better at '
        'statistics than any programmer and better at '
        'programming than any statistician.',
    "!false (It's funny because it's true.)",
    'Why do programmers always mix up Christmas and '
        'Halloween? Because Dec 25 is Oct 31.',
    'Have you tried turning it off and on again?'
]


def get_version():
    """Returns a string with the Python version used by the
    Pyodide runtime.
    """
    return 'Python ' + version.split()[0]


def get_date_and_time():
    """Returns a string with the current date and time using the
    ISO 8601 format.
    """
    now = datetime.now()
    result = now.isoformat()
    return result


def get_quote():
    """Obtains and returns a string with a funny random oneline
    quote.
    """
    return choice(ONELINERS)


if __name__ == '__main__':
    # Some simple tests to make sure that the code works as expected.
    print(get_version())
    print(get_date_and_time())
    print(get_quote())
