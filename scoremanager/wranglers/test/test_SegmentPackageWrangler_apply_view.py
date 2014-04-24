# -*- encoding: utf-8 -*-
import pytest
pytest.skip('make me work')
from abjad import *
import scoremanager

# must have is_test=False to test views
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_SegmentPackageWrangler_apply_view_01():
    r'''In library. Applies view.
    
    Makes sure only one segment package is visible after view is applied.
    '''
    
    input_ = 'g vnew _test rm all'
    input_ += ' add segment~01~(Red~Example~Score) done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_user_input=input_)
    applied_view = score_manager._transcript[-8]

    lines = [
        'Score manager - segments (_test)',
        '',
        '   1: segment 01 (Red Example Score)',
        '',
        '      segments - copy (cp)',
        '      segments - new (new)',
        '      segments - remove (rm)',
        '      segments - rename (ren)',
        '',
        ]
    assert applied_view.lines == lines


#def test_SegmentPackageWrangler_apply_view_02():
#    r'''In score package. Applies view.
#    
#    Makes sure only one stylesheet is visible after view is applied.
#    '''
#    
#    input_ = 'ssx red~example~score g vnew _test'
#    input_ += ' rm all add stylesheet-addendum.ily done default'
#    input_ += ' va _test vrm _test default q'
#    score_manager._run(pending_user_input=input_)
#    applied_view = score_manager._transcript[-8]
#
#    lines = [
#        'Red Example Score (2013) - segments (_test)',
#        '',
#        '   1: stylesheet-addendum.ily',
#        '',
#        '      segments - copy (cp)',
#        '      segments - new (new)',
#        '      segments - remove (rm)',
#        '      segments - rename (ren)',
#        '',
#        ]
#    assert applied_view.lines == lines