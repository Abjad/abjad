# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageManager_edit_year_of_completion_01():

    try:
        score_manager = scoremanager.core.ScoreManager(is_test=True)
        input_ = 'red~example~score setup year 2001 q'
        score_manager._run(pending_user_input=input_, is_test=True)
        transcript = score_manager._transcript
        assert transcript.signature == (9,)
        assert transcript[-5].title == 'Red Example Score (2013) - setup'
        assert transcript.last_title == 'Red Example Score (2001) - setup'
    finally:
        input_ = "red~example~score setup year 2013 q"
        score_manager._run(pending_user_input=input_, is_test=True)
        transcript = score_manager._transcript
        assert transcript.signature == (9,)
        string = 'Red Example Score (2001) - setup'
        assert transcript[-5].title == string
        string = 'Red Example Score (2013) - setup'
        assert transcript.last_title == string
