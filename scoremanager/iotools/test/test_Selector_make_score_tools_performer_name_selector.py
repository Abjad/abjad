# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_score_tools_performer_name_selector_01():

    selector = scoremanager.iotools.Selector
    selector = selector.make_score_tools_performer_name_selector()
    selector._session._is_test = True
    input_ = 'q'
    assert selector._run(pending_user_input=input_) is None

    selector = scoremanager.iotools.Selector
    selector = selector.make_score_tools_performer_name_selector()
    selector._session._is_test = True
    input_ = 'b'
    assert selector._run(pending_user_input=input_) is None

    selector = scoremanager.iotools.Selector
    selector = selector.make_score_tools_performer_name_selector()
    selector._session._is_test = True
    input_ = 'h'
    assert selector._run(pending_user_input=input_) is None


def test_Selector_make_score_tools_performer_name_selector_02():

    selector = scoremanager.iotools.Selector
    selector = selector.make_score_tools_performer_name_selector()
    selector._session._is_test = True
    input_ = 'vn'
    assert selector._run(pending_user_input=input_) == 'violinist'


def test_Selector_make_score_tools_performer_name_selector_03():

    selector = scoremanager.iotools.Selector
    selector = selector.make_score_tools_performer_name_selector()
    selector._session._is_test = True
    selector.is_ranged = True
    result = ['violinist', 'violist']
    input_ = 'vn, va'
    assert selector._run(pending_user_input=input_) == result
