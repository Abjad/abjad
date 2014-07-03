# -*- encoding: utf-8 -*-
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


def test_systemtools_TestManager_compare_pys_01():
    r'''True when lines are exactly the same.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = ["print 'hello'"]
        second_lines = first_lines[:]
        file(path_1, 'w').write('\n'.join(first_lines))
        file(path_2, 'w').write('\n'.join(second_lines))
        assert systemtools.TestManager.compare_pys(path_1, path_2)


def test_systemtools_TestManager_compare_pys_02():
    r'''True when white space differs.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = ["print 'hello'", '', '', "print 'goodbye'", '']
        second_lines = ['', "print 'hello'", "print 'goodbye'"]
        file(path_1, 'w').write('\n'.join(first_lines))
        file(path_2, 'w').write('\n'.join(second_lines))
        assert systemtools.TestManager.compare_lys(path_1, path_2)


def test_systemtools_TestManager_compare_pys_03():
    r'''False when any other lines differ.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        first_lines = ["print 'hello'"]
        second_lines = ["print 'goodbye'"]
        file(path_1, 'w').write('\n'.join(first_lines))
        file(path_2, 'w').write('\n'.join(second_lines))
        assert not systemtools.TestManager.compare_lys(path_1, path_2)