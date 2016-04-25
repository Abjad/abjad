# -*- coding: utf-8 -*-
import os
from abjad import *
configuration = systemtools.AbjadConfiguration()

path_1 = os.path.join(
    configuration.abjad_directory,
    'test_1.py',
    )
path_2 = os.path.join(
    configuration.abjad_directory,
    'test_2.py',
    )


def test_systemtools_TestManager__compare_text_files_01():
    r'''True when lines are exactly the same.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = ["print 'hello'"]
        second_lines = first_lines[:]
        with open(path_1, 'w') as file_pointer:
            file_pointer.write('\n'.join(first_lines))
        with open(path_2, 'w') as file_pointer:
            file_pointer.write('\n'.join(second_lines))
        assert systemtools.TestManager._compare_text_files(path_1, path_2)


def test_systemtools_TestManager__compare_text_files_02():
    r'''True when white space differs.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = ["print 'hello'", '', '', "print 'goodbye'", '']
        second_lines = ['', "print 'hello'", "print 'goodbye'"]
        with open(path_1, 'w') as file_pointer:
            file_pointer.write('\n'.join(first_lines))
        with open(path_2, 'w') as file_pointer:
            file_pointer.write('\n'.join(second_lines))
        assert systemtools.TestManager._compare_text_files(path_1, path_2)


def test_systemtools_TestManager__compare_text_files_03():
    r'''False when any other lines differ.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = ["print 'hello'"]
        second_lines = ["print 'goodbye'"]
        with open(path_1, 'w') as file_pointer:
            file_pointer.write('\n'.join(first_lines))
        with open(path_2, 'w') as file_pointer:
            file_pointer.write('\n'.join(second_lines))
        assert not systemtools.TestManager._compare_text_files(path_1, path_2)
