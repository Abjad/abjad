# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_FileManager__remove_01():
    r'''Nonversioned file.
    '''

    path = os.path.join(
        configuration.score_manager_directory_path, 
        'temporary_file.txt',
        )
    session = scoremanager.core.Session(is_test=True)
    manager = scoremanager.managers.FileManager(path=path, session=session)

    assert not os.path.exists(path)
    try:
        manager._make_empty_asset()
        assert os.path.exists(path)
        manager._remove()
        assert not os.path.exists(path)
    finally:
        if os.path.exists(path):
            os.remove(path)
    assert not os.path.exists(path)


def test_FileManager__remove_02():
    r'''Versioned file.
    '''

    path = os.path.join(
        configuration.score_manager_directory_path, 
        'temporary_file.txt',
        )
    session = scoremanager.core.Session(is_test=True)
    manager = scoremanager.managers.FileManager(path=path, session=session)

    assert not os.path.exists(path)
    try:
        manager._make_empty_asset()
        assert os.path.exists(path)
        manager.add()
        assert manager._is_in_git_repository()
        assert manager._is_git_added()
        manager._remove()
        assert not os.path.exists(path)
    finally:
        if os.path.exists(path):
            os.remove(path)
    assert not os.path.exists(path)
