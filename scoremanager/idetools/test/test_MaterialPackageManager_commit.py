# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_commit_01():

    wrangler = ide._material_package_wrangler
    manager = wrangler._find_git_manager()

    manager._session._is_repository_test = True
    manager.commit()
    assert manager._session._attempted_to_commit


def test_MaterialPackageManager_commit_02():

    wrangler = ide._material_package_wrangler
    manager = wrangler._find_svn_manager()

    if not manager:
        return

    manager._session._is_repository_test = True
    manager.commit()
    assert manager._session._attempted_to_commit