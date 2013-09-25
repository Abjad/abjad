# -*- encoding: utf-8 -*-
from experimental import *
from experimental.tools.scoremanagertools.selectors import Selector


def test_Selector_make_articulation_handler_selector_01():

    selector = Selector.make_articulation_handler_selector()
    string = 'experimental.tools.scoremanagertools.materialpackages.red_mar'
    result = selector._run(pending_user_input=string) 

    package = 'experimental.tools.scoremanagertools'
    package += '.materialpackages.red_marcati'
    assert result == package
