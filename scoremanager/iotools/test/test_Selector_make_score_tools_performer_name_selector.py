# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
from scoremanager.iotools import Selector


def test_Selector_make_score_tools_performer_name_selector_01():

    selector = Selector.make_score_tools_performer_name_selector()
    assert selector._run(pending_user_input='q') is None

    selector = Selector.make_score_tools_performer_name_selector()
    assert selector._run(pending_user_input='b') is None

    selector = Selector.make_score_tools_performer_name_selector()
    assert selector._run(pending_user_input='home') is None


def test_Selector_make_score_tools_performer_name_selector_02():

    selector = Selector.make_score_tools_performer_name_selector()
    assert selector._run(pending_user_input='vn') == 'violinist'


def test_Selector_make_score_tools_performer_name_selector_03():

    selector = Selector.make_score_tools_performer_name_selector()
    selector.is_ranged = True
    assert selector._run(pending_user_input='vn, va') == ['violinist', 'violist']
