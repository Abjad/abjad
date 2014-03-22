# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()
session = scoremanager.core.Session()
score_manager = scoremanager.core.ScoreManager(is_test=True)
#wrangler = scoremanager.wranglers.SegmentPackageWrangler(session=session)


def test_SegmentPackageWrangler__find_up_to_date_versioned_manager_01():
    r'''Works with Git.
    '''

    wrangler = score_manager._segment_package_wrangler
    manager = wrangler._find_up_to_date_versioned_manager(
        repository='git',
        system=True,
        )

    assert isinstance(manager, scoremanager.managers.SegmentPackageManager)
    assert manager._is_git_versioned()
    assert manager._is_up_to_date()
    assert os.path.basename(os.path.dirname(manager._path)) == 'segments'
    assert not os.path.basename(manager._path) == 'segments'


def test_SegmentPackageWrangler__find_up_to_date_versioned_manager_02():
    r'''Works with Subversion.
    '''

    wrangler = score_manager._segment_package_wrangler
    manager = wrangler._find_up_to_date_versioned_manager(
        system=False,
        repository='svn',
        )

    if not manager:
        return

    assert isinstance(manager, scoremanager.managers.SegmentPackageManager)
    assert manager._is_svn_versioned()
    assert manager._is_up_to_date()
    assert os.path.basename(os.path.dirname(manager._path)) == 'segments'
    assert not os.path.basename(manager._path) == 'segments'