# -*- encoding: utf-8 -*-
from abjad import *


def test_chordtools_Chord___str___01():

    chord = Chord("<ef' cs'' f''>4")

    assert str(chord) == "<ef' cs'' f''>4"
