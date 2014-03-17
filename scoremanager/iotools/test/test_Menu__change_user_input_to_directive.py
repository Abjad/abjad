# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager()


def test_Menu__change_user_input_to_directive_01():
    r'''Works with accented characters.
    '''

    score_manager._run(pending_user_input='étude q', is_test=True)
    string = 'Étude Example Score (2013)'
    assert score_manager._transcript.last_title == string


def test_Menu__change_user_input_to_directive_02():
    r'''Works without accented characters.
    '''

    score_manager._run(pending_user_input='etude q', is_test=True)
    string = 'Étude Example Score (2013)'
    assert score_manager._transcript.last_title == string
