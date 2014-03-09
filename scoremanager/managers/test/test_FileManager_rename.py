# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_FileManager_rename_01():
    r'''Nonversioned file.
    '''

    path = os.path.join(
        configuration.score_manager_directory_path, 
        'test_file.txt',
        )
    new_path = os.path.join(
        configuration.score_manager_directory_path, 
        'new_test_file.txt',
        )
    file_manager = scoremanager.managers.FileManager(path=path)

    assert not os.path.exists(path)
    assert not os.path.exists(new_path)
    try:
        file_manager._make_empty_asset()
        assert os.path.exists(path)
        file_manager.rename(pending_user_input='new_test_file.txt y q')
        assert file_manager._path == new_path
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


def test_FileManager_rename_02():
    r'''Versioned file.
    '''

    path = os.path.join(
        configuration.score_manager_directory_path, 
        'test_file.txt',
        )
    new_path = os.path.join(
        configuration.score_manager_directory_path, 
        'new_test_file.txt',
        )
    file_manager = scoremanager.managers.FileManager(path=path)
    input_ = 'new_test_file.txt y q'

    assert not os.path.exists(path)
    assert not os.path.exists(new_path)
    try:
        file_manager._make_empty_asset()
        assert os.path.exists(path)
        file_manager.add()
        assert file_manager._is_git_added()
        assert not file_manager._is_git_versioned()
        file_manager.rename(pending_user_input=input_)
        assert file_manager._path == new_path
        assert os.path.exists(new_path)
        file_manager._remove()
    finally:
        if os.path.exists(path):
            os.remove(path)
        if os.path.exists(new_path):
            os.remove(new_path)
    assert not os.path.exists(path)
    assert not os.path.exists(new_path)
