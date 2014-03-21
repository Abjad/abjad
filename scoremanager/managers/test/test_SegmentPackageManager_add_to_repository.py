# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()
session = scoremanager.core.Session
wrangler = scoremanager.wranglers.SegmentPackageWrangler(session=session)


def test_SegmentPackageManager_add_to_repository_01():
    r'''Add two files to Git-managed segment package.
    Make sure Git recognizes the files as added.
    Then unadd the files and leave the segment package as found.
    '''

    manager = wrangler._find_up_to_date_versioned_manager(
        system=True,
        repository='git',
        )

    assert manager._test_add_to_repository()
    

def test_SegmentPackageManager_add_to_repository_02():
    r'''Add two files to Subversioned-managed segment package.
    Make sure Subversion recognizes the files as added.
    Then unadd the file and leave the score package as found.
    '''

    manager = wrangler._find_up_to_date_versioned_manager(
        system=False,
        repository='svn',
        )
            
    if not manager:
        return

    assert manager._test_add_to_repository()