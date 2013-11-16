# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_apply_accidental_to_named_pitch_01():

    assert pitchtools.apply_accidental_to_named_pitch(
        NamedPitch('cs', 4), 'sharp') == NamedPitch('css', 4)
    assert pitchtools.apply_accidental_to_named_pitch(
        NamedPitch('cs', 4), 'flat') == NamedPitch('c', 4)
    assert pitchtools.apply_accidental_to_named_pitch(
        NamedPitch('cs', 4), 'natural') == NamedPitch('cs', 4)
    assert pitchtools.apply_accidental_to_named_pitch(
        NamedPitch('cs', 4), 'quarter sharp') == NamedPitch('ctqs', 4)
