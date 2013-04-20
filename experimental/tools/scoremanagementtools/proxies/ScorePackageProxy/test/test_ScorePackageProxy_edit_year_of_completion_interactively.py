# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageProxy_edit_year_of_completion_interactively_01():

    try:
        score_manager = scoremanagementtools.studio.ScoreManager()
        score_manager.run(user_input='example~score~i setup year 2001 q')
        assert score_manager.ts == (9,)
        assert score_manager.transcript[-5][0] == 'Example Score I (2013) - setup'
        assert score_manager.transcript[-2][0] == 'Example Score I (2001) - setup'
    finally:
        score_manager.run(user_input="example~score~i setup year 2013 q")
        assert score_manager.ts == (9,)
        assert score_manager.transcript[-5][0] == 'Example Score I (2001) - setup'
        assert score_manager.transcript[-2][0] == 'Example Score I (2013) - setup'
