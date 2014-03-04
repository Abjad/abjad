# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_FileManager__rename_01():
    r'''Nonversioned file.
    '''

    configuration = scoremanager.core.ScoreManagerConfiguration()
    path = os.path.join(
        configuration.score_manager_directory_path, 
        'temporary_file.txt',
        )
    file_manager = scoremanager.managers.FileManager(
        path=path)
    assert not os.path.exists(path)

    try:
        file_manager._make_empty_asset()
        assert os.path.exists(path)
        new_path = os.path.join(
            configuration.score_manager_directory_path, 
            'new_temporary_file.txt',
            )
        file_manager._rename(new_path)
        assert not os.path.exists(path)
        assert os.path.exists(new_path)
        file_manager._remove()
    finally:
        if os.path.exists(path):
            os.remove(path)
        if os.path.exists(new_path):
            os.remove(new_path)
        assert not os.path.exists(path)
        assert not os.path.exists(new_path)


def test_FileManager__rename_02():
    r'''Versioned file.
    '''

    configuration = scoremanager.core.ScoreManagerConfiguration()
    path = os.path.join(
        configuration.score_manager_directory_path, 
        'temporary_file.txt',
        )
    file_manager = scoremanager.managers.FileManager(
        path=path)
    assert not os.path.exists(path)

    try:
        file_manager._make_empty_asset()
        assert os.path.exists(path)
        file_manager.add_assets_to_repository()
        assert file_manager._is_git_added()
        assert not file_manager._is_git_versioned()
        new_path = os.path.join(
            configuration.score_manager_directory_path, 
            'new_temporary_file.txt',
            )
        file_manager._rename(new_path)
        assert os.path.exists(new_path)
        assert file_manager._path == new_path
    finally:
        file_manager._remove()
        assert not os.path.exists(path)
        assert not os.path.exists(new_path)
