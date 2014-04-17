# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_StylesheetWrangler_apply_view_01():
    r'''Makes sure only one stylesheet is visible with view.
    '''
    
    input_ = 'y vnew _test rm all add clean-letter-14.ily done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_user_input=input_)
    applied_view = score_manager._transcript[-8]

    lines = [
        'Score manager - stylesheet library (_test view)',
        '',
        '    1: clean-letter-14.ily (Abjad)',
        '',
        '    stylesheets - copy (cp)',
        '    stylesheets - new (new)',
        '    stylesheets - remove (rm)',
        '    stylesheets - rename (ren)',
        '',
        ]
    assert applied_view.lines == lines