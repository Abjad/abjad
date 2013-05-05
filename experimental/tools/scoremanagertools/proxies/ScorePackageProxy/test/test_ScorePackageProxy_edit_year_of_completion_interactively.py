# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageProxy_edit_year_of_completion_interactively_01():

    try:
        score_manager = scoremanagertools.scoremanager.ScoreManager()
        score_manager.run(user_input='example~score~i setup year 2001 q')
        assert score_manager.session.transcript.signature == (9,)
        assert score_manager.session.transcript[-5][1][0] == 'Example Score I (2013) - setup'
        assert score_manager.session.transcript[-2][1][0] == 'Example Score I (2001) - setup'
    finally:
        score_manager.run(user_input="example~score~i setup year 2013 q")
        assert score_manager.session.transcript.signature == (9,)
        assert score_manager.session.transcript[-5][1][0] == 'Example Score I (2001) - setup'
        assert score_manager.session.transcript[-2][1][0] == 'Example Score I (2013) - setup'
