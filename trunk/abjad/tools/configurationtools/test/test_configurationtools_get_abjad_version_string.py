from abjad import *
from abjad.tools import configurationtools


def test_configurationtools_get_abjad_version_string_01():

    assert isinstance(configurationtools.get_abjad_version_string(), str)
