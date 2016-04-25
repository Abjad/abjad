# -*- coding: utf-8 -*-
import os
from abjad import *
configuration = systemtools.AbjadConfiguration()

path_1 = os.path.join(
    configuration.abjad_directory,
    'test_1.ly',
    )
path_2 = os.path.join(
    configuration.abjad_directory,
    'test_2.ly',
    )

lines = [
    r'\language "english"',
    '',
    r'\new Staff {',
    "    c'4",
    "    d'4",
    "    e'4",
    "    f'4",
    ]


def test_systemtools_TestManager__compare_lys_01():
    r'''True when lines are exactly the same.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = [r'\version "2.19.7"'] + lines
        second_lines = first_lines[:]
        with open(path_1, 'w') as file_pointer:
            file_pointer.write('\n'.join(first_lines))
        with open(path_2, 'w') as file_pointer:
            file_pointer.write('\n'.join(second_lines))
        assert systemtools.TestManager._compare_lys(path_1, path_2)


def test_systemtools_TestManager__compare_lys_02():
    r'''True when version strings differ.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = [r'\version "2.19.7"'] + lines
        second_lines = [r'\version "2.19.8"'] + lines
        with open(path_1, 'w') as file_pointer:
            file_pointer.write('\n'.join(first_lines))
        with open(path_2, 'w') as file_pointer:
            file_pointer.write('\n'.join(second_lines))
        assert systemtools.TestManager._compare_lys(path_1, path_2)


def test_systemtools_TestManager__compare_lys_03():
    r'''True when comments differ.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = [r'\version "2.19.7"'] + lines
        second_lines = ['% 2014-01-01 05:43:01', r'\version "2.19.8"'] + lines
        with open(path_1, 'w') as file_pointer:
            file_pointer.write('\n'.join(first_lines))
        with open(path_2, 'w') as file_pointer:
            file_pointer.write('\n'.join(second_lines))
        assert systemtools.TestManager._compare_lys(path_1, path_2)


def test_systemtools_TestManager__compare_lys_04():
    r'''False when any other lines differ.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = [r'\version "2.19.7"'] + lines
        second_lines = [r'\version "2.19.8"'] + lines + ['foo']
        with open(path_1, 'w') as file_pointer:
            file_pointer.write('\n'.join(first_lines))
        with open(path_2, 'w') as file_pointer:
            file_pointer.write('\n'.join(second_lines))
        assert not systemtools.TestManager._compare_lys(path_1, path_2)
