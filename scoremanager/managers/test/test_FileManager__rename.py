# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_FileManager__rename_01():
    r'''Nonversioned file.
    '''

    path = os.path.join(
        configuration.score_manager_directory_path, 
        'temporary-file.txt',
        )
    new_path = os.path.join(
        configuration.score_manager_directory_path, 
        'new_temporary_file.txt',
        )
    session = scoremanager.core.Session(is_test=True)
    manager = scoremanager.managers.FileManager(path=path, session=session)

    assert not os.path.exists(path)
    assert not os.path.exists(new_path)
    try:
        manager._make_empty_asset()
        assert os.path.exists(path)
        manager._rename(new_path)
        assert not os.path.exists(path)
        assert os.path.exists(new_path)
        manager._remove()
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

    path = os.path.join(
        configuration.score_manager_directory_path, 
        'temporary-file.txt',
        )
    new_path = os.path.join(
        configuration.score_manager_directory_path, 
        'new_temporary_file.txt',
        )
    session = scoremanager.core.Session(is_test=True)
    manager = scoremanager.managers.FileManager(path=path, session=session)

    assert not os.path.exists(path)
    assert not os.path.exists(new_path)
    try:
        manager._make_empty_asset()
        assert os.path.exists(path)
        manager.add(prompt=False)
        assert manager._is_in_git_repository()
        assert manager._is_git_added()
        manager._rename(new_path)
        assert os.path.exists(new_path)
        assert manager._path == new_path
        manager._remove()
    finally:
        if os.path.exists(path):
            os.remove(path)
        if os.path.exists(new_path):
            os.remove(new_path)
    assert not os.path.exists(path)
    assert not os.path.exists(new_path)
