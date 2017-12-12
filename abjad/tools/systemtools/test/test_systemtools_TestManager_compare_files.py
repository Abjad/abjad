import os
import abjad
from abjad.tools import systemtools
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


def test_systemtools_TestManager_compare_files_01():
    r'''Is true when lines are exactly the same.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = [r'\version "2.19.7"'] + lines
        second_lines = first_lines[:]
        with open(path_1, 'w') as file_pointer:
            file_pointer.write('\n'.join(first_lines))
        with open(path_2, 'w') as file_pointer:
            file_pointer.write('\n'.join(second_lines))
        assert systemtools.TestManager._compare_lys(path_1, path_2)


def test_systemtools_TestManager_compare_files_02():
    r'''Is true when version strings differ.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = [r'\version "2.19.7"'] + lines
        second_lines = [r'\version "2.19.8"'] + lines
        with open(path_1, 'w') as file_pointer:
            file_pointer.write('\n'.join(first_lines))
        with open(path_2, 'w') as file_pointer:
            file_pointer.write('\n'.join(second_lines))
        assert systemtools.TestManager._compare_lys(path_1, path_2)


def test_systemtools_TestManager_compare_files_03():
    r'''Is true when comments differ.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = [r'\version "2.19.7"'] + lines
        second_lines = ['% 2014-01-01 05:43:01', r'\version "2.19.8"'] + lines
        with open(path_1, 'w') as file_pointer:
            file_pointer.write('\n'.join(first_lines))
        with open(path_2, 'w') as file_pointer:
            file_pointer.write('\n'.join(second_lines))
        assert systemtools.TestManager._compare_lys(path_1, path_2)


def test_systemtools_TestManager_compare_files_04():
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


### TEXT FILES ###

path_1 = os.path.join(
    configuration.abjad_directory,
    'test_1.py',
    )
path_2 = os.path.join(
    configuration.abjad_directory,
    'test_2.py',
    )

def test_systemtools_TestManager_compare_files_05():
    r'''Is true when lines are exactly the same.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = ["print 'hello'"]
        second_lines = first_lines[:]
        with open(path_1, 'w') as file_pointer:
            file_pointer.write('\n'.join(first_lines))
        with open(path_2, 'w') as file_pointer:
            file_pointer.write('\n'.join(second_lines))
        assert systemtools.TestManager._compare_text_files(path_1, path_2)


def test_systemtools_TestManager_compare_files_06():
    r'''Is true when white space differs.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = ["print 'hello'", '', '', "print 'goodbye'", '']
        second_lines = ['', "print 'hello'", "print 'goodbye'"]
        with open(path_1, 'w') as file_pointer:
            file_pointer.write('\n'.join(first_lines))
        with open(path_2, 'w') as file_pointer:
            file_pointer.write('\n'.join(second_lines))
        assert systemtools.TestManager._compare_text_files(path_1, path_2)


def test_systemtools_TestManager_compare_files_07():
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
