# -*- encoding: utf-8 -*-
from experimental import *
from scoremanager.iotools import Selector


def test_Selector_make_score_instrument_selector_01():

    session = scoremanager.core.Session()
    session.snake_case_current_score_name = 'red_example_score'
    selector = Selector.make_score_instrument_selector(session=session)

    assert selector._run(pending_user_input='vio') == instrumenttools.Violin()
    assert selector._run(pending_user_input='oth') == 'other'
