# -*- encoding: utf-8 -*-
from abjad import *


def test_systemtools_AbjadConfiguration_list_abjad_environment_variables_01():

    environment_variables = \
        systemtools.AbjadConfiguration.list_abjad_environment_variables()

    assert all(isinstance(x, tuple) for x in environment_variables)
