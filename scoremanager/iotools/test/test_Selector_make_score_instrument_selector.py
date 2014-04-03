# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_score_instrument_selector_01():

    session = scoremanager.core.Session(is_test=True)
    session._set_test_score('red_example_score')
    selector = scoremanager.iotools.Selector()
    selector = selector.make_score_instrument_selector(session=session)
    selector._session._is_test = True

    input_ = 'vio'
    result = selector._run(pending_user_input=input_) 
    assert result == instrumenttools.Violin()

    input_ = 'oth'
    result = selector._run(pending_user_input=input_) 
    assert result == 'other'