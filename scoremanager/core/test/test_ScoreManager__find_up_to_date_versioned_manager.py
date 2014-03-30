# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScoreManager__find_up_to_date_versioned_manager_01():
    r'''Works for Git-managed build directory.
    '''

    manager = score_manager._find_up_to_date_manager(
        scoremanager.managers.BuildDirectoryManager,
        system=True,
        repository='git',
        )

    assert isinstance(manager, scoremanager.managers.BuildDirectoryManager)
    assert manager._is_git_versioned()
    assert manager._is_up_to_date()
    assert os.path.basename(manager._path) == 'build'


def test_ScoreManager__find_up_to_date_versioned_manager_02():
    r'''Works for Subversion-managed build directory.
    '''

    manager = score_manager._find_up_to_date_manager(
        scoremanager.managers.BuildDirectoryManager,
        system=False,
        repository='svn',
        )

    if not manager:
        return

    assert isinstance(manager, scoremanager.managers.BuildDirectoryManager)
    assert manager._is_svn_versioned()
    assert manager._is_up_to_date()
    assert os.path.basename(manager._path) == 'build'