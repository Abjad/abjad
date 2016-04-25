# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitch_apply_accidental_01():

    assert pitchtools.NumberedPitch(12).apply_accidental('sharp') == 13
    assert pitchtools.NumberedPitch(12).apply_accidental('flat') == 11
    assert pitchtools.NumberedPitch(12).apply_accidental('natural') == 12


def test_pitchtools_NumberedPitch_apply_accidental_02():

    assert pitchtools.NumberedPitch(12).apply_accidental('quarter sharp') == 12.5
    assert pitchtools.NumberedPitch(12).apply_accidental('quarter flat') == 11.5
