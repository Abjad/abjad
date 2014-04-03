# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_tempo_selector_01():

    session = scoremanager.core.Session(is_test=True)
    session._set_test_score('red_example_score')
    selector = scoremanager.iotools.Selector()
    selector = selector.make_tempo_selector(session=session)
    selector._session._is_test = True
    input_ = '8=72'
    result = selector._run(pending_user_input=input_)

    tempo = indicatortools.Tempo(durationtools.Duration(1, 8), 72)
    assert result == tempo