# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_commit_01():
    r'''Flow control reaches Git-managed score package.
    '''

    manager = ide._score_package_wrangler._find_up_to_date_manager(
        repository='git',
        system=True,
        )

    manager._session._is_repository_test = True
    manager.commit()
    assert manager._session._attempted_to_commit


def test_ScorePackageManager_commit_02():
    r'''Flow control reaches Subversion-managed score package.
    '''

    manager = ide._score_package_wrangler._find_up_to_date_manager(
        repository='svn',
        system=False,
        )

    if not manager:
        return

    manager._session._is_repository_test = True
    manager.commit()
    assert manager._session._attempted_to_commit