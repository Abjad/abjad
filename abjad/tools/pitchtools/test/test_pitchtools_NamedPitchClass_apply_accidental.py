# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitchClass_apply_accidental_01():

    pc = pitchtools.NamedPitchClass('cs')

    assert pc.apply_accidental('sharp') == pitchtools.NamedPitchClass('css')
    assert pc.apply_accidental('flat') == pitchtools.NamedPitchClass('c')
    assert pc.apply_accidental('natural') == pitchtools.NamedPitchClass('cs')
