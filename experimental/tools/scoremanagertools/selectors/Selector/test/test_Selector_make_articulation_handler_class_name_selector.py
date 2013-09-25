# -*- encoding: utf-8 -*-
from experimental import *
from experimental.tools.scoremanagertools.selectors import Selector


def test_Selector_make_articulation_handler_class_name_selector_01():

    selector = Selector.make_articulation_handler_class_name_selector()
    result = selector._run(pending_user_input='reiterated') 

    assert result == 'ReiteratedArticulationHandler'
