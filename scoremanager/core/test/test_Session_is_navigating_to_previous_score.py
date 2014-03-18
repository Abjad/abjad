# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Session_is_navigating_to_previous_score_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    string = 'stp stp q'
    score_manager._run(pending_user_input=string, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Étude Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles
