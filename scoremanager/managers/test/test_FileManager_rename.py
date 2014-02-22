# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_FileManager_rename_01():
    r'''Nonversioned file.
    '''

    configuration = scoremanager.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        configuration.score_manager_directory_path, 
        'temporary_file.txt',
        )
    file_manager = scoremanager.managers.FileManager(
        filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_manager._make_empty_asset()
        assert os.path.exists(filesystem_path)
        new_filesystem_path = os.path.join(
            configuration.score_manager_directory_path, 
            'new_temporary_file.txt',
            )
        file_manager._rename(new_filesystem_path)
        assert not os.path.exists(filesystem_path)
        assert os.path.exists(new_filesystem_path)
        file_manager._remove()
    finally:
        if os.path.exists(filesystem_path):
            os.remove(filesystem_path)
        if os.path.exists(new_filesystem_path):
            os.remove(new_filesystem_path)
        assert not os.path.exists(filesystem_path)
        assert not os.path.exists(new_filesystem_path)


def test_FileManager_rename_02():
    r'''Versioned file.
    '''

    configuration = scoremanager.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        configuration.score_manager_directory_path, 
        'temporary_file.txt',
        )
    file_manager = scoremanager.managers.FileManager(
        filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_manager._make_empty_asset()
        assert os.path.exists(filesystem_path)
        file_manager.add_assets_to_repository()
        assert file_manager._is_versioned()
        new_filesystem_path = os.path.join(
            configuration.score_manager_directory_path, 
            'new_temporary_file.txt',
            )
        file_manager._rename(new_filesystem_path)
        assert os.path.exists(new_filesystem_path)
        assert file_manager.filesystem_path == new_filesystem_path
    finally:
        file_manager._remove()
        assert not os.path.exists(filesystem_path)
        assert not os.path.exists(new_filesystem_path)
