# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_StylesheetFileWrangler_run_01():
    r'''Entries are annotated with labels like (Abjad).
    '''
    
    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='ylm q')
    line = '     1: clean-letter-14.ily (Abjad)'
    assert line in score_manager.session.io_transcript.last_menu_lines
