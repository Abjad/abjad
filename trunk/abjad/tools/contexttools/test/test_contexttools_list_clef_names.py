from abjad import *


def test_contexttools_list_clef_names_01():

    assert 'treble' in contexttools.list_clef_names()
