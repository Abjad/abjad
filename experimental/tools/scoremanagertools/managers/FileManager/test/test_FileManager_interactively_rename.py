# -*- encoding: utf-8 -*-
import os
from experimental import *
import py.test


@py.test.skip('FIXME: Broken by class package flattening.')
def test_FileManager_interactively_rename_01():
    r'''Nonversioned file.
    '''

    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 'test_file.txt')
    file_manager = scoremanagertools.managers.FileManager(filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_manager._make_empty_asset()
        assert os.path.exists(filesystem_path)
        assert not file_manager._is_versioned()
        new_filesystem_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path, 'new_test_file.txt')
        file_manager.interactively_rename(pending_user_input='new_test_file.txt y q')
        assert file_manager.filesystem_path == new_filesystem_path
        assert not os.path.exists(filesystem_path)
        assert os.path.exists(new_filesystem_path)
    finally:
        file_manager._remove()
        assert not os.path.exists(filesystem_path)
        assert not os.path.exists(new_filesystem_path)


def test_FileManager_interactively_rename_02():
    r'''Versioned file.
    '''

    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 'test_file.txt')
    file_manager = scoremanagertools.managers.FileManager(filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_manager._make_empty_asset()
        assert os.path.exists(filesystem_path)
        file_manager.repository_add()
        assert file_manager._is_versioned()
        new_filesystem_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path, 'new_test_file.txt')
        file_manager.interactively_rename(pending_user_input='new_test_file.txt y q')
        assert file_manager.filesystem_path == new_filesystem_path
        assert os.path.exists(new_filesystem_path)
    finally:
        file_manager._remove()
        assert not os.path.exists(filesystem_path)
        assert not os.path.exists(new_filesystem_path)
