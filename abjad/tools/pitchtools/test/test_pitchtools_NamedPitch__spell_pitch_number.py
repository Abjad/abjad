# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitch__spell_pitch_number_01():

    accidental = NamedPitch._spell_pitch_number(12, 'b')
    assert accidental == (pitchtools.Accidental('s'), 4)
    accidental = NamedPitch._spell_pitch_number(12, 'c')
    assert accidental == (pitchtools.Accidental(''), 5)
    accidental = NamedPitch._spell_pitch_number(12, 'd')
    assert accidental == (pitchtools.Accidental('ff'), 5)


def test_pitchtools_NamedPitch__spell_pitch_number_02():

    accidental = NamedPitch._spell_pitch_number(13, 'b')
    assert accidental == (pitchtools.Accidental('ss'), 4)
    accidental = NamedPitch._spell_pitch_number(13, 'c')
    assert accidental == (pitchtools.Accidental('s'), 5)
    accidental = NamedPitch._spell_pitch_number(13, 'd')
    assert accidental == (pitchtools.Accidental('f'), 5)


def test_pitchtools_NamedPitch__spell_pitch_number_03():

    t = NamedPitch._spell_pitch_number(14, 'c')
    assert t == (pitchtools.Accidental('ss'), 5)
    t = NamedPitch._spell_pitch_number(14, 'd')
    assert t == (pitchtools.Accidental(''), 5)
    t = NamedPitch._spell_pitch_number(14, 'e')
    assert t == (pitchtools.Accidental('ff'), 5)
