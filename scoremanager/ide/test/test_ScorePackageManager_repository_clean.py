# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_ScorePackageManager_repository_clean_01():

    wrangler = score_manager._score_package_wrangler
    manager = wrangler._find_git_manager()

    assert manager._test_repository_clean()


def test_ScorePackageManager_repository_clean_02():

    wrangler = score_manager._score_package_wrangler
    manager = wrangler._find_svn_manager()

    if not manager:
        return

    assert manager._test_repository_clean()