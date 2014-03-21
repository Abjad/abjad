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

    manager = score_manager._find_up_to_date_versioned_manager(
        scoremanager.managers.ScorePackageManager,
        configuration.abjad_score_packages_directory_path,
        repository='git',
        )

    assert manager._test_add_to_repository()


def test_ScorePackageManager_add_to_repository_02():
    r'''Add two files to Subversioned-managed score package.
    Make sure Subversion recognizes the files as added.
    Then unadd the file and leave the score package as found.
    '''

    manager = score_manager._find_up_to_date_versioned_manager(
        scoremanager.managers.ScorePackageManager,
        configuration.user_score_packages_directory_path,
        repository='svn',
        )

    if not manager:
        return

    assert manager._test_add_to_repository()