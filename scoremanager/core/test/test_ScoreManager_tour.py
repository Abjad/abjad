# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager_tour_01():
    r'''stn score.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'stn stn q'
    score_manager._run(pending_user_input=string, is_test=True)
    titles = [
        'Score manager - example scores',
        'Blue Example Score (2013)',
        'Étude Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles


def test_ScoreManager_tour_02():
    r'''Previous score.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'stp stp q'
    score_manager._run(pending_user_input=string, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Étude Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles
