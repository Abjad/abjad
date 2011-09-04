from abjad import *
from abjad.tools import configurationtools


def test_configurationtools_list_abjad_templates_01():

    templates = configurationtools.list_abjad_templates()

    assert all([isinstance(x, str) for x in templates])
