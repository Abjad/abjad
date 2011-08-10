from abjad import *
from abjad.tools import cfgtools


def test_cfgtools_get_abjad_revision_string_01( ):


    assert isinstance(cfgtools.get_abjad_revision_string( ), str)
