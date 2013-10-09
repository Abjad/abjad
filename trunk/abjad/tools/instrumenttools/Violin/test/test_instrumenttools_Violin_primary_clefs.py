# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Violin_primary_clefs_01():

    violin = instrumenttools.Violin()

    assert violin.starting_clefs == [contexttools.ClefMark('treble')]
