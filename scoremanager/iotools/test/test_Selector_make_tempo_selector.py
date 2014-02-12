# -*- encoding: utf-8 -*-
from experimental import *
from scoremanager.iotools import Selector


def test_Selector_make_tempo_selector_01():

    session = scoremanager.core.Session()
    session._snake_case_current_score_name = 'red_example_score'
    selector = Selector.make_tempo_selector(session=session)
    result = selector._run(pending_user_input='8=72')

    tempo = indicatortools.Tempo(durationtools.Duration(1, 8), 72)
    assert result == tempo
