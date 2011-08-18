from abjad import *


def test_instrumenttools_Violin_all_clefs_01():

    violin = instrumenttools.Violin()

    assert violin.all_clefs == [contexttools.ClefMark('treble')]
