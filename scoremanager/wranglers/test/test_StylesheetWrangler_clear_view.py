# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must be is_test=False to test view application
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_StylesheetWrangler_clear_view_01():
    r'''Makes sure more than one stylesheet is visible without view.
    '''
    
    input_ = 'y vnew _test rm all add clean-letter-14.ily done default'
    input_ += ' va _test vc vrm _test default q'
    score_manager._run(pending_input=input_)
    transcript = score_manager._transcript

    lines = [
        'Score manager - stylesheets (_test)',
        '',
        '   1: clean-letter-14.ily (Abjad)',
        '',
        '      stylesheets - copy (cp)',
        '      stylesheets - new (new)',
        '      stylesheets - remove (rm)',
        '      stylesheets - rename (ren)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)