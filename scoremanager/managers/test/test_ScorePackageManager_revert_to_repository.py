# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager_revert_to_repository_01():

    manager = score_manager._find_up_to_date_manager(
        scoremanager.managers.ScorePackageManager,
        repository='git',
        system=True,
        )

    assert manager._test_revert_to_repository()


def test_ScorePackageManager_revert_to_repository_02():

    manager = score_manager._find_up_to_date_manager(
        scoremanager.managers.ScorePackageManager,
        repository='svn',
        system=False,
        )

    if not manager:
        return

    assert manager._test_revert_to_repository()