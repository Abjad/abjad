# -*- encoding: utf-8 -*-
from experimental import *
from experimental.tools.scoremanagertools.selectors import Selector


def test_Selector_make_instrument_tools_instrument_name_selector_01():

    selector = Selector.make_instrument_tools_instrument_name_selector()
    assert selector._run(pending_user_input='marimba') == 'marimba'
