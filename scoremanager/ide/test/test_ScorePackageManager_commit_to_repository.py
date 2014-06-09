# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_ScorePackageManager_commit_to_repository_01():
    r'''Flow control reaches Git-managed score package.
    '''

    manager = score_manager._score_package_wrangler._find_up_to_date_manager(
        repository='git',
        system=True,
        )

    manager._session._is_repository_test = True
    manager.commit_to_repository()
    assert manager._session._attempted_to_commit_to_repository


def test_ScorePackageManager_commit_to_repository_02():
    r'''Flow control reaches Subversion-managed score package.
    '''

    manager = score_manager._score_package_wrangler._find_up_to_date_manager(
        repository='svn',
        system=False,
        )

    if not manager:
        return

    manager._session._is_repository_test = True
    manager.commit_to_repository()
    assert manager._session._attempted_to_commit_to_repository