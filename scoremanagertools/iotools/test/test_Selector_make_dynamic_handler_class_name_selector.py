# -*- encoding: utf-8 -*-
from experimental import *
from scoremanagertools.iotools import Selector


def test_Selector_make_dynamic_handler_class_name_selector_01():

    selector = Selector.make_dynamic_handler_class_name_selector()

    result = selector._run(pending_user_input='terraced') 
    assert result == 'TerracedDynamicsHandler'
