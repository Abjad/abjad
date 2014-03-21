# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()
session = scoremanager.core.Session()
wrangler = scoremanager.wranglers.ScorePackageWrangler(session=session)


def test_ScorePackageWrangler__find_up_to_date_versioned_manager_01():
    r'''Works with Git.
    '''

    manager = wrangler._find_up_to_date_versioned_manager(
        system=True,
        repository='git',
        )

    storehouse = configuration.abjad_score_packages_directory_path

    assert isinstance(manager, scoremanager.managers.ScorePackageManager)
    assert manager._is_git_versioned()
    assert manager._is_up_to_date()
    assert manager._path.startswith(storehouse)
    assert not manager._path == storehouse


def test_ScorePackageWrangler__find_up_to_date_versioned_manager_02():
    r'''Works with Subversion.
    '''

    manager = wrangler._find_up_to_date_versioned_manager(
        system=False,
        repository='svn',
        )

    if not manager:
        return

    storehouse = configuration.user_score_packages_directory_path

    assert isinstance(manager, scoremanager.managers.ScorePackageManager)
    assert manager._is_svn_versioned()
    assert manager._is_up_to_date()
    assert manager._path.startswith(storehouse)
    assert not manager._path == storehouse