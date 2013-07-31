# -*- encoding: utf-8 -*-
from experimental import *


def test_ParameterSpecifierClassNameSelector_run_01():

    selector = scoremanagertools.selectors.ParameterSpecifierClassNameSelector()
    assert selector._run(pending_user_input='troping') == 'TropingSpecifier'
