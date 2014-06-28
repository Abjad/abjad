# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_PackageManager__repository_add_command_01():

    manager = ide._score_package_wrangler._find_up_to_date_manager(
        repository='git',
        system=True,
        )

    command = 'git add -A {}'.format(manager._path)
    assert manager._repository_add_command == command


def test_PackageManager__repository_add_command_02():

    manager = ide._score_package_wrangler._find_up_to_date_manager(
        repository='svn',
        system=False,
        )

    if not manager:
        return

    assert manager._is_up_to_date()
    temporary_file = os.path.join(manager._path, 'test_temporary.txt')
    assert not os.path.exists(temporary_file)
    with systemtools.FilesystemState(remove=[temporary_file]):
        with open(temporary_file, 'w') as file_pointer:
            file_pointer.write('')
        assert os.path.isfile(temporary_file)
        assert manager._get_unadded_asset_paths() == [temporary_file]
        command = 'svn add {}'.format(temporary_file)
        assert manager._repository_add_command == command