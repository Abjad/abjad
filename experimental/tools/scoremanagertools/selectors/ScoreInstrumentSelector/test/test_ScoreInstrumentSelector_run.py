# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *


def test_ScoreInstrumentSelector_run_01():

    selector = scoremanagertools.selectors.ScoreInstrumentSelector()
    selector.session.snake_case_current_score_name = 'red_example_score'

    assert selector._run(pending_user_input='vio') == instrumenttools.Violin()
    assert selector._run(pending_user_input='oth') == 'other'
