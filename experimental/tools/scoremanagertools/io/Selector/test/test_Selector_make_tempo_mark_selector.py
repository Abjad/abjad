# -*- encoding: utf-8 -*-
from experimental import *
from experimental.tools.scoremanagertools.io import Selector


def test_Selector_make_tempo_mark_selector_01():

    session = scoremanagertools.scoremanager.Session()
    session._snake_case_current_score_name = 'red_example_score'
    selector = Selector.make_tempo_mark_selector(session=session)
    result = selector._run(pending_user_input='8=72')

    tempo_mark = contexttools.TempoMark(durationtools.Duration(1, 8), 72)
    assert result == tempo_mark
