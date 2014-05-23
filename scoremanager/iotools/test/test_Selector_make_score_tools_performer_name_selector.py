# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.core.Session(is_test=True)


def test_Selector_make_score_tools_performer_name_selector_01():

    selector = scoremanager.iotools.Selector(session=session)
    selector = selector.make_score_tools_performer_name_selector()
    selector._session._is_test = True
    input_ = 'q'
    assert selector._run(input_=input_) is None

    selector = selector.make_score_tools_performer_name_selector()
    selector._session._is_test = True
    input_ = 'b'
    assert selector._run(input_=input_) is None

    selector = selector.make_score_tools_performer_name_selector()
    selector._session._is_test = True
    input_ = 'h'
    assert selector._run(input_=input_) is None


def test_Selector_make_score_tools_performer_name_selector_02():

    session._reinitialize()
    selector = scoremanager.iotools.Selector(session=session)
    selector = selector.make_score_tools_performer_name_selector()
    selector._session._is_test = True
    input_ = 'vn'
    assert selector._run(input_=input_) == 'violinist'


def test_Selector_make_score_tools_performer_name_selector_03():

    session._reinitialize()
    selector = scoremanager.iotools.Selector(session=session)
    selector = selector.make_score_tools_performer_name_selector(
        is_ranged=True)
    selector._session._is_test = True
    result = ['violinist', 'violist']
    input_ = 'vn, va'
    assert selector._run(input_=input_) == result