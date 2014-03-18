# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_score_instrument_selector_01():

    session = scoremanager.core.Session(is_test=True)
    session._current_score_snake_case_name = 'red_example_score'
    selector = scoremanager.iotools.Selector
    selector = selector.make_score_instrument_selector(session=session)

    input_ = 'vio'
    assert selector._run(pending_user_input=input_) == instrumenttools.Violin()

    input_ = 'oth'
    assert selector._run(pending_user_input=input_) == 'other'
