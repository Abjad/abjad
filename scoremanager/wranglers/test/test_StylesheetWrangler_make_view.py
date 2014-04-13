# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_make_view_01():
    r'''Title is correct.
    '''

    input_ = 'y vn test~view q' 
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    string = 'Score manager - stylesheet library - views - test view - edit'
    assert transcript.last_title == string


def test_StylesheetWrangler_make_view_02():
    r'''Includes all stylesheets.

    Test checks to make sure at least one Abjad stylesheet appears.
    '''

    input_ = 'y vn test_view q' 
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    string = 'clean-letter-14.ily (Abjad)'
    assert string in transcript.contents