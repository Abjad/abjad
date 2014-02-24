# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_dynamic_handler_class_name_selector_01():

    selector = scoremanager.iotools.Selector
    selector = selector.make_dynamic_handler_class_name_selector()
    selector._run(pending_user_input='q') 
    transcript = selector._transcript

    assert transcript.last_menu_lines == [
        'Select:', 
        '', 
        '     1: ReiteratedDynamicHandler', 
        '     2: TerracedDynamicsHandler', 
        '',
        ]


def test_Selector_make_dynamic_handler_class_name_selector_02():

    selector = scoremanager.iotools.Selector
    selector = selector.make_dynamic_handler_class_name_selector()

    result = selector._run(pending_user_input='terraced') 
    assert result == 'TerracedDynamicsHandler'
