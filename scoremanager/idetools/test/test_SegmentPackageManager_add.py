# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_add_01():
    r'''Add two files to Git-managed segment package.
    Make sure Git recognizes the files as added.
    Then unadd the files and leave the segment package as found.
    '''

    wrangler = ide._segment_package_wrangler
    manager = wrangler._find_git_manager()

    assert manager._test_add()


def test_SegmentPackageManager_add_02():
    r'''Add two files to Subversioned-managed segment package.
    Make sure Subversion recognizes the files as added.
    Then unadd the file and leave the score package as found.
    '''

    wrangler = ide._segment_package_wrangler
    manager = wrangler._find_svn_manager()

    if not manager:
        return

    assert manager._test_add()