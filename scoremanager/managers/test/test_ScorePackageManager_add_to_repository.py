# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()
score_manager = scoremanager.core.ScoreManager()


def test_ScorePackageManager_add_to_repository_01():
    r'''Add two files to Git-managed score package.
    Make sure Git recognizes the files as added.
    Then unadd the files and leave the score package as found.
    '''

    manager = score_manager._find_up_to_date_manager(
        scoremanager.managers.ScorePackageManager,
        repository='git',
        system=True,
        )

    assert manager._test_add_to_repository()


def test_ScorePackageManager_add_to_repository_02():
    r'''Add two files to Subversioned-managed score package.
    Make sure Subversion recognizes the files as added.
    Then unadd the file and leave the score package as found.
    '''

    manager = score_manager._find_up_to_date_manager(
        scoremanager.managers.ScorePackageManager,
        repository='svn',
        system=False,
        )

    if not manager:
        return

    assert manager._test_add_to_repository()