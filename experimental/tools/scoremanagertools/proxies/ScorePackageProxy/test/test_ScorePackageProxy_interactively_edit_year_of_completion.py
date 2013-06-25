# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageProxy_interactively_edit_year_of_completion_01():

    try:
        score_manager = scoremanagertools.scoremanager.ScoreManager()
        score_manager._run(pending_user_input='red~example~score setup year 2001 q')
        assert score_manager.session.transcript.signature == (9,)
        assert score_manager.session.transcript[-5][1][0] == 'Red Example Score (2013) - setup'
        assert score_manager.session.transcript[-2][1][0] == 'Red Example Score (2001) - setup'
    finally:
        score_manager._run(pending_user_input="red~example~score setup year 2013 q")
        assert score_manager.session.transcript.signature == (9,)
        assert score_manager.session.transcript[-5][1][0] == 'Red Example Score (2001) - setup'
        assert score_manager.session.transcript[-2][1][0] == 'Red Example Score (2013) - setup'
