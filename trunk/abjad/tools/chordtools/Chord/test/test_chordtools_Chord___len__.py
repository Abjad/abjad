# -*- encoding: utf-8 -*-
from abjad import *


def test_chordtools_Chord___len___01():

    assert len(Chord('<>4')) == 0
    assert len(Chord("<ef'>4")) == 1
    assert len(Chord("<ef' cs''>4")) == 2
    assert len(Chord("<ef' cs'' f''>4")) == 3
