# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_score_instrument_selector_01():

    session = scoremanager.core.Session()
    session._current_score_snake_case_name = 'red_example_score'
    selector = scoremanager.iotools.Selector
    selector = selector.make_score_instrument_selector(session=session)

    assert selector._run(pending_user_input='vio') == instrumenttools.Violin()
    assert selector._run(pending_user_input='oth') == 'other'
