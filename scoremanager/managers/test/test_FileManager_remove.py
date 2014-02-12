# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_FileManager_remove_01():
    r'''Nonversioned file.
    '''

    score_manager_configuration = scoremanager.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 
        'temporary_file.txt',
        )
    file_manager = scoremanager.managers.FileManager(
        filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_manager._make_empty_asset()
        assert os.path.exists(filesystem_path)
        file_manager._remove()
        assert not os.path.exists(filesystem_path)
    finally:
        if os.path.exists(filesystem_path):
            os.remove(filesystem_path)
        assert not os.path.exists(filesystem_path)


def test_FileManager_remove_02():
    r'''Versioned file.
    '''

    score_manager_configuration = scoremanager.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 
        'temporary_file.txt',
        )
    file_manager = scoremanager.managers.FileManager(
        filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_manager._make_empty_asset()
        assert os.path.exists(filesystem_path)
        file_manager.repository_add()
        assert file_manager._is_versioned()
        file_manager._remove()
        assert not os.path.exists(filesystem_path)
    finally:
        if os.path.exists(filesystem_path):
            os.remove(filesystem_path)
        assert not os.path.exists(filesystem_path)
