# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must have is_test=False to test view application
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_SegmentPackageWrangler_apply_view_01():
    r'''In library. Applies view.
    
    Makes sure only one segment is visible after view is applied.
    '''
    
    input_ = 'g vnew _test rm all'
    input_ += ' add A~(Red~Example~Score) done default'
    input_ += ' vap _test vrm _test default q'
    score_manager._run(pending_input=input_)
    transcript = score_manager._transcript

    lines = [
        'Score Manager - segments (_test)',
        '',
        '   1: A (Red Example Score)',
        '',
        '      segments - copy (cp)',
        '      segments - new (new)',
        '      segments - remove (rm)',
        '      segments - rename (ren)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)


def test_SegmentPackageWrangler_apply_view_02():
    r'''In score package. Applies view.
    
    Makes sure only one segment is visible after view is applied.
    '''
    
    input_ = 'red~example~score g vnew _test'
    input_ += ' rm all add A done default'
    input_ += ' vap _test vrm _test default q'
    score_manager._run(pending_input=input_)
    transcript = score_manager._transcript

    lines = [
        'Red Example Score (2013) - segments (_test)',
        '',
        '   1: A',
        '',
        '      segments - copy (cp)',
        '      segments - new (new)',
        '      segments - remove (rm)',
        '      segments - rename (ren)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)