# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_dynamic_handler_class_name_selector_01():

    session = scoremanager.core.Session(is_test=True)
    selector = scoremanager.iotools.Selector(session=session)
    selector = selector.make_dynamic_handler_class_name_selector()
    selector._session._is_test = True
    input_ = 'q'
    selector._run(input_=input_)
    transcript = selector._transcript

    assert transcript.last_menu_lines == [
        'Select:',
        '',
        '   1: ReiteratedDynamicHandler',
        '   2: TerracedDynamicsHandler',
        '',
        ]


def test_Selector_make_dynamic_handler_class_name_selector_02():

    session = scoremanager.core.Session(is_test=True)
    selector = scoremanager.iotools.Selector(session=session)
    selector = selector.make_dynamic_handler_class_name_selector()
    selector._session._is_test = True

    input_ = 'terraced'
    result = selector._run(input_=input_)
    assert result == 'TerracedDynamicsHandler'