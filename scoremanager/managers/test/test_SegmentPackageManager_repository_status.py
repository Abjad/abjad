# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_repository_status_01():
    r'''Works with Git.
    '''

    input_ = 'red~example~score g rst default q'
    score_manager._run(pending_user_input=input_)
    string = '# On branch master'

    assert string in score_manager._transcript.titles


def test_SegmentPackageManager_repository_status_02():
    r'''Works with Subversion.
    '''

    wrangler = score_manager._segment_package_wrangler
    manager = wrangler._find_svn_manager()
    if not manager:
        return

    manager.repository_status(prompt=False)
    titles = manager._transcript.titles

    assert titles[0].endswith('...')
    assert titles[1] == ''
    assert len(titles) == 2