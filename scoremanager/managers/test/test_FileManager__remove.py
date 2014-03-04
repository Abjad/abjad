# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_FileManager__remove_01():
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
        file_manager._remove()
        assert not os.path.exists(path)
    finally:
        if os.path.exists(path):
            os.remove(path)
        assert not os.path.exists(path)


def test_FileManager__remove_02():
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
        assert file_manager._is_git_added()
        assert not file_manager._is_git_versioned()
        file_manager._remove()
        assert not os.path.exists(path)
    finally:
        if os.path.exists(path):
            os.remove(path)
        assert not os.path.exists(path)
