# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_commit_to_repository_01():

    wrangler = score_manager._material_package_wrangler
    manager = wrangler._find_git_manager()

    manager._session._is_repository_test = True
    manager.commit_to_repository(prompt=False)
    assert manager._session._attempted_to_commit_to_repository


def test_MaterialPackageManager_commit_to_repository_02():

    wrangler = score_manager._material_package_wrangler
    manager = wrangler._find_svn_manager()

    if not manager:
        return

    manager._session._is_repository_test = True
    manager.commit_to_repository(prompt=False)
    assert manager._session._attempted_to_commit_to_repository