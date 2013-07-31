# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import configurationtools


def test_AbjadConfiguration_list_abjad_environment_variables_01():

    environment_variables = \
        configurationtools.AbjadConfiguration.list_abjad_environment_variables()

    assert all(isinstance(x, tuple) for x in environment_variables)
