# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_dynamic_handler_class_name_selector_01():

    session = scoremanager.idetools.Session(is_test=True)
    selector = scoremanager.idetools.Selector(session=session)
    selector = selector.make_dynamic_handler_class_name_selector()
    selector._session._is_test = True
    selector._session._pending_input = 'q'
    selector._run()
    contents = selector._transcript.contents

    lines = [
        'Select:',
        '',
        '   1: ReiteratedDynamicHandler',
        '   2: TerracedDynamicsHandler',
        '',
        ]
    for line in lines:
        assert line in contents


def test_Selector_make_dynamic_handler_class_name_selector_02():

    session = scoremanager.idetools.Session(is_test=True)
    selector = scoremanager.idetools.Selector(session=session)
    selector = selector.make_dynamic_handler_class_name_selector()
    selector._session._is_test = True
    selector._session._pending_input = 'terraced'
    result = selector._run()

    assert result == 'TerracedDynamicsHandler'