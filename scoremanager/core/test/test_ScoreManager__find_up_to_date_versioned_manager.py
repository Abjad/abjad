# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()
score_manager = scoremanager.core.ScoreManager()


def test_ScoreManager__find_up_to_date_versioned_manager_01():
    r'''Works for Git-managed build directory.
    '''

    manager = score_manager._find_up_to_date_versioned_manager(
        scoremanager.managers.BuildDirectoryManager,
        suffix='build',
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

    manager = score_manager._find_up_to_date_versioned_manager(
        scoremanager.managers.BuildDirectoryManager,
        suffix='build',
        system=False,
        repository='svn',
        )

    if not manager:
        return

    assert isinstance(manager, scoremanager.managers.BuildDirectoryManager)
    assert manager._is_svn_versioned()
    assert manager._is_up_to_date()
    assert os.path.basename(manager._path) == 'build'


def test_ScoreManager__find_up_to_date_versioned_manager_03():
    r'''Works for Git-managed distribution directory.
    '''

    manager = score_manager._find_up_to_date_versioned_manager(
        scoremanager.managers.DistributionDirectoryManager,
        suffix='distribution',
        system=True,
        repository='git',
        )

    assert isinstance(
        manager, 
        scoremanager.managers.DistributionDirectoryManager,
        )
    assert manager._is_git_versioned()
    assert manager._is_up_to_date()
    assert os.path.basename(manager._path) == 'distribution'


def test_ScoreManager__find_up_to_date_versioned_manager_04():
    r'''Works for Subversion-managed build directory.
    '''

    manager = score_manager._find_up_to_date_versioned_manager(
        scoremanager.managers.DistributionDirectoryManager,
        suffix='distribution',
        system=False,
        repository='svn',
        )

    if not manager:
        return

    assert isinstance(
        manager, 
        scoremanager.managers.DistributionDirectoryManager,
        )
    assert manager._is_svn_versioned()
    assert manager._is_up_to_date()
    assert os.path.basename(manager._path) == 'distribution'