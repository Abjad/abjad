from abjad import *
from abjad.tools import configurationtools


def test_configurationtools_get_text_editor_01():

    assert isinstance(configurationtools.get_text_editor(), str)
