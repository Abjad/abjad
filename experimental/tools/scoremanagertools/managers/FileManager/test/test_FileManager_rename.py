# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_FileManager_rename_01():
    r'''Nonversioned file.
    '''

    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 'temporary_file.txt')
    file_manager = scoremanagertools.managers.FileManager(filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_manager.make_empty_asset()
        assert os.path.exists(filesystem_path)
        assert not file_manager.is_versioned()
        new_filesystem_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path, 'new_temporary_file.txt')
        file_manager.rename(new_filesystem_path)
        assert not os.path.exists(filesystem_path)
        assert os.path.exists(new_filesystem_path)
        file_manager.remove()
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

    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 'temporary_file.txt')
    file_manager = scoremanagertools.managers.FileManager(filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_manager.make_empty_asset()
        assert os.path.exists(filesystem_path)
        file_manager.repository_add()
        assert file_manager.is_versioned()
        new_filesystem_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path, 'new_temporary_file.txt')
        file_manager.rename(new_filesystem_path)
        assert os.path.exists(new_filesystem_path)
        assert file_manager.filesystem_path == new_filesystem_path
    finally:
        file_manager.remove()
        assert not os.path.exists(filesystem_path)
        assert not os.path.exists(new_filesystem_path)
