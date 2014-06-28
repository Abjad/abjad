# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_revert_01():

    wrangler = ide._segment_package_wrangler
    manager = wrangler._find_git_manager(must_have_file=True)

    assert manager._test_revert()


def test_SegmentPackageManager_revert_02():

    wrangler = ide._segment_package_wrangler
    manager = wrangler._find_svn_manager(must_have_file=True)

    if not manager:
        return

    assert manager._test_revert()