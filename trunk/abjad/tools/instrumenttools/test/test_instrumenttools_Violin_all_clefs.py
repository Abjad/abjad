# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Violin_all_clefs_01():

    violin = instrumenttools.Violin()

    assert violin.allowable_clefs == [contexttools.ClefMark('treble')]
