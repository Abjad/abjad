# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
from scoremanager.iotools import Selector


def test_Selector_make_parameter_specifier_class_name_selector_01():

    selector = Selector.make_parameter_specifier_class_name_selector()

    assert selector._run(pending_user_input='artic') == 'ArticulationSpecifier'
