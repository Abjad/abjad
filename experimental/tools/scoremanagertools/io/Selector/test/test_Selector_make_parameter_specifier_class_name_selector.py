# -*- encoding: utf-8 -*-
from experimental import *
from experimental.tools.scoremanagertools.io import Selector


def test_Selector_make_parameter_specifier_class_name_selector_01():

    selector = Selector.make_parameter_specifier_class_name_selector()

    assert selector._run(pending_user_input='troping') == 'TropingSpecifier'
