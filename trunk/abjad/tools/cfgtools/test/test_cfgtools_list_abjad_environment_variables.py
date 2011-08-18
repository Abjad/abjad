from abjad import *
from abjad.tools import cfgtools


def test_cfgtools_list_abjad_environment_variables_01():

    environment_variables = cfgtools.list_abjad_environment_variables()

    assert all([isinstance(x, tuple) for x in environment_variables])
