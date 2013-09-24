# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageProxy_interactively_edit_year_of_completion_01():

    try:
        score_manager = scoremanagertools.scoremanager.ScoreManager()
        user_input = 'red~example~score score~setup year 2001 q'
        score_manager._run(pending_user_input=user_input)
        io_transcript = score_manager.session.io_transcript
        assert io_transcript.signature == (9,)
        assert io_transcript[-5][1][0] == 'Red Example Score (2013) - setup'
        assert io_transcript[-2][1][0] == 'Red Example Score (2001) - setup'
    finally:
        user_input = "red~example~score score~setup year 2013 q"
        score_manager._run(pending_user_input=user_input)
        io_transcript = score_manager.session.io_transcript
        assert io_transcript.signature == (9,)
        assert io_transcript[-5][1][0] == 'Red Example Score (2001) - setup'
        assert io_transcript[-2][1][0] == 'Red Example Score (2013) - setup'
