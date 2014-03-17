# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Session_command_repetition_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='stn . . . q', is_test=True)
    titles = [ 
        'Score manager - example scores',
        'Blue Example Score (2013)',
        'Étude Example Score (2013)',
        'Red Example Score (2013)',
        'Blue Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles
