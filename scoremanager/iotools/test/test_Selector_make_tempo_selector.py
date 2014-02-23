# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_tempo_selector_01():

    session = scoremanager.core.Session()
    session._current_score_snake_case_name = 'red_example_score'
    selector = scoremanager.iotools.Selector
    selector = selector.make_tempo_selector(session=session)
    result = selector._run(pending_user_input='8=72')

    tempo = indicatortools.Tempo(durationtools.Duration(1, 8), 72)
    assert result == tempo
