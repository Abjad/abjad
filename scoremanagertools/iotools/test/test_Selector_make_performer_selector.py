# -*- encoding: utf-8 -*-
from experimental import *
from scoremanagertools.iotools import Selector


def test_Selector_make_performer_selector_01():

    session = scoremanagertools.scoremanager.Session()
    session.snake_case_current_score_name = 'red_example_score'
    selector = Selector.make_performer_selector(session=session)
    result = selector._run(pending_user_input='hornist')

    performer = instrumenttools.Performer(
        name='hornist', 
        instruments=[instrumenttools.FrenchHorn()]
        )
    assert result == performer
