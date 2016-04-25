# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitchClass_apply_accidental_01():

    pc = pitchtools.NumberedPitchClass(11)

    assert pc.apply_accidental('sharp') == pitchtools.NumberedPitchClass(0)
    assert pc.apply_accidental('flat') == pitchtools.NumberedPitchClass(10)
    assert pc.apply_accidental('double sharp') == pitchtools.NumberedPitchClass(1)
    assert pc.apply_accidental('double flat') == pitchtools.NumberedPitchClass(9)
    assert pc.apply_accidental('quarter sharp') == pitchtools.NumberedPitchClass(11.5)
    assert pc.apply_accidental('quarter flat') == pitchtools.NumberedPitchClass(10.5)
