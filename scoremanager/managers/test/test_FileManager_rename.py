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
        'test_file.txt',
        )
    file_manager = scoremanager.managers.FileManager(
        filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_manager._make_empty_asset()
        assert os.path.exists(filesystem_path)
        new_filesystem_path = os.path.join(
            configuration.score_manager_directory_path, 
            'new_test_file.txt',
            )
        file_manager.rename(
            pending_user_input='new_test_file.txt y q')
        assert file_manager._filesystem_path == new_filesystem_path
        assert not os.path.exists(filesystem_path)
        assert os.path.exists(new_filesystem_path)
    finally:
        file_manager._remove()
        assert not os.path.exists(filesystem_path)
        assert not os.path.exists(new_filesystem_path)


def test_FileManager_rename_02():
    r'''Versioned file.
    '''

    configuration = scoremanager.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        configuration.score_manager_directory_path, 
        'test_file.txt',
        )
    file_manager = scoremanager.managers.FileManager(
        filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_manager._make_empty_asset()
        assert os.path.exists(filesystem_path)
        file_manager.add_assets_to_repository()
        assert file_manager._is_git_added()
        assert not file_manager._is_git_versioned()
        new_filesystem_path = os.path.join(
            configuration.score_manager_directory_path, 
            'new_test_file.txt',
            )
        string = 'new_test_file.txt y q'
        file_manager.rename(pending_user_input=string)
        assert file_manager._filesystem_path == new_filesystem_path
        assert os.path.exists(new_filesystem_path)
    finally:
        file_manager._remove()
        assert not os.path.exists(filesystem_path)
        assert not os.path.exists(new_filesystem_path)
