from abjad import *
from abjad.tools import cfgtools


def test_cfgtools_list_abjad_templates_01():

    templates = cfgtools.list_abjad_templates()

    assert all([isinstance(x, str) for x in templates])
