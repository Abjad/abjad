# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_StylesheetFileWrangler__run_01():
    r'''Entries are annotated with labels like (Abjad).
    '''
    
    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='lmy q')
    line = '     1: clean-letter-14.ily (Abjad)'
    assert line in score_manager._transcript.last_menu_lines
