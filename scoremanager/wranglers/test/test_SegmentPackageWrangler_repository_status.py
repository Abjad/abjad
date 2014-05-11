# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_repository_status_01():
    r'''Works with library.
    '''

    input_ = 'g rst q'
    score_manager._run(pending_input=input_)
    title = '# On branch master'

    assert title in score_manager._transcript.titles


def test_SegmentPackageWrangler_repository_status_02():
    r'''Works with Git-managed segment package.
    '''

    input_ = 'red~example~score g rst q'
    score_manager._run(pending_input=input_)
    title = '# On branch master'

    assert title in score_manager._transcript.titles


def test_SegmentPackageWrangler_repository_status_03():
    r'''Works with Subversion-managed segment package.
    '''

    wrangler = score_manager._segment_package_wrangler
    manager = wrangler._find_svn_manager(inside_score=False)
    if not manager:
        return

    manager.repository_status()
    titles = manager._transcript.titles

    assert titles[0].endswith('...')
    assert titles[1] == ''
    assert len(titles) == 2