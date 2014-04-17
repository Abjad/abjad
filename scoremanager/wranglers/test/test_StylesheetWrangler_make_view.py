# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_make_view_01():
    r'''Makes sure view creation menu title is correct.
    '''

    input_ = 'y vnew _test q' 
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    string = 'Score manager - stylesheet library - views - _test view - edit:'
    assert transcript.last_title == string


def test_StylesheetWrangler_make_view_02():
    r'''Checks to make sure at least one Abjad stylesheet appears in
    view creation menu.
    '''

    input_ = 'y vnew _test q' 
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    string = 'clean-letter-14.ily (Abjad)'
    assert string in transcript.contents