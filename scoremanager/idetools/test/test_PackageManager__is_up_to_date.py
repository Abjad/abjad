# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_PackageManager__is_up_to_date_01():

    manager = ide._score_package_wrangler._find_up_to_date_manager(
        repository='git',
        system=True,
        )
    temporary_file = os.path.join(manager._path, 'test_temporary.txt')

    assert manager._is_up_to_date()
    assert not os.path.exists(temporary_file)

    with systemtools.FilesystemState(remove=[temporary_file]):
        with open(temporary_file, 'w') as file_pointer:
            file_pointer.write('')
        assert os.path.isfile(temporary_file)
        assert not manager._is_up_to_date()


def test_PackageManager__is_up_to_date_02():

    manager = ide._score_package_wrangler._find_up_to_date_manager(
        repository='svn',
        system=False,
        )
    
    if not manager:
        return

    temporary_file = os.path.join(manager._path, 'test_temporary.txt')

    assert manager._is_up_to_date()
    assert not os.path.exists(temporary_file)

    with systemtools.FilesystemState(remove=[temporary_file]):
        with open(temporary_file, 'w') as file_pointer:
            file_pointer.write('')
        assert os.path.isfile(temporary_file)
        assert not manager._is_up_to_date()