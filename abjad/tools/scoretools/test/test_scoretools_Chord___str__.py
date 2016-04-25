# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Chord___str___01():

    chord = Chord("<ef' cs'' f''>4")

    assert str(chord) == "<ef' cs'' f''>4"
