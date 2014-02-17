# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_score_tools_performer_name_selector_01():

    selector = scoremanager.iotools.Selector
    selector = selector.make_score_tools_performer_name_selector()
    assert selector._run(pending_user_input='q') is None

    selector = scoremanager.iotools.Selector
    selector = selector.make_score_tools_performer_name_selector()
    assert selector._run(pending_user_input='b') is None

    selector = scoremanager.iotools.Selector
    selector = selector.make_score_tools_performer_name_selector()
    assert selector._run(pending_user_input='home') is None


def test_Selector_make_score_tools_performer_name_selector_02():

    selector = scoremanager.iotools.Selector
    selector = selector.make_score_tools_performer_name_selector()
    assert selector._run(pending_user_input='vn') == 'violinist'


def test_Selector_make_score_tools_performer_name_selector_03():

    selector = scoremanager.iotools.Selector
    selector = selector.make_score_tools_performer_name_selector()
    selector.is_ranged = True
    result = ['violinist', 'violist']
    assert selector._run(pending_user_input='vn, va') == result
