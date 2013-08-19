# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitchVector___init___01():

    ncpv = pitchtools.NamedPitchVector(["c''", "c''", "cs''", "cs''", "cs''"])

    assert sorted(ncpv.items()) == [("c''", 2), ("cs''", 3)]
