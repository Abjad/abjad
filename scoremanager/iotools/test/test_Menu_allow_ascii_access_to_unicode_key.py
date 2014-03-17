# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager()


def test_Menu_allow_ascii_access_to_unicode_key_01():

    score_manager._run(pending_user_input='étude q', is_test=True)
    string = 'Étude Example Score (2013)'
    assert score_manager._transcript.last_title == string


def test_Menu_allow_ascii_access_to_unicode_key_02():

    score_manager._run(pending_user_input='etude q', is_test=True)
    string = 'Étude Example Score (2013)'
    assert score_manager._transcript.last_title == string
