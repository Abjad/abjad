# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_StylesheetWrangler_apply_view_01():
    r'''Makes view. Applies view.
    '''
    
    input_ = 'y vnew _test rm all add clean-letter-14.ily done default q'
    score_manager._run(pending_user_input=input_)
    input_ = 'y va _test q'
    score_manager._run(pending_user_input=input_)
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

    assert score_manager._transcript[-2].lines == lines

    input_ = 'y vrm _test default q'
    score_manager._run(pending_user_input=input_)
    
    title = 'Score manager - stylesheet library'
    assert score_manager._transcript.last_title == title