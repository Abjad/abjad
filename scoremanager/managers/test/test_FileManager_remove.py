# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_FileManager_remove_01():
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
        file_manager.remove(
            pending_user_input='remove default q')
        assert not os.path.exists(path)
    finally:
        if os.path.exists(path):
            os.remove(path)
        assert not os.path.exists(path)


def test_FileManager_remove_02():
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
        file_manager.add()
        file_manager.remove(
            pending_user_input='remove default q')
        assert not os.path.exists(path)
    finally:
        if os.path.exists(path):
            os.remove(path)
        assert not os.path.exists(path)
