# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageManager_interactively_edit_year_of_completion_01():

    try:
        score_manager = scoremanager.core.ScoreManager()
        user_input = 'red~example~score setup year 2001 q'
        score_manager._run(pending_user_input=user_input)
        io_transcript = score_manager.session.io_transcript
        assert io_transcript.signature == (9,)
        assert io_transcript[-5].title == 'Red Example Score (2013) - setup'
        assert io_transcript.last_menu_title == 'Red Example Score (2001) - setup'
    finally:
        user_input = "red~example~score setup year 2013 q"
        score_manager._run(pending_user_input=user_input)
        io_transcript = score_manager.session.io_transcript
        assert io_transcript.signature == (9,)
        string = 'Red Example Score (2001) - setup'
        assert io_transcript[-5].title == string
        string = 'Red Example Score (2013) - setup'
        assert io_transcript.last_menu_title == string
