# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_revert_to_repository_01():

    wrangler = score_manager._segment_package_wrangler
    manager = wrangler._find_git_manager(must_have_file=True)

    assert manager._test_revert_to_repository()


def test_SegmentPackageManager_revert_to_repository_02():

    wrangler = score_manager._segment_package_wrangler
    manager = wrangler._find_svn_manager(must_have_file=True)

    if not manager:
        return

    assert manager._test_revert_to_repository()