# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_StylesheetWrangler__run_01():
    r'''Entries are annotated with labels like (Abjad).
    '''
    
    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'y q'
    score_manager._run(pending_user_input=input_)
    line = '    1: clean-letter-14.ily (Abjad)'
    assert line in score_manager._transcript.last_menu_lines
