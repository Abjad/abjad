# -*- coding: utf-8 -*-
import abjad


def test_pitchtools_NamedPitch__spell_pitch_number_01():

    accidental = abjad.NamedPitch._spell_pitch_number(12, 'b')
    assert accidental == (abjad.Accidental('s'), 4)
    accidental = abjad.NamedPitch._spell_pitch_number(12, 'c')
    assert accidental == (abjad.Accidental(''), 5)
    accidental = abjad.NamedPitch._spell_pitch_number(12, 'd')
    assert accidental == (abjad.Accidental('ff'), 5)


def test_pitchtools_NamedPitch__spell_pitch_number_02():

    accidental = abjad.NamedPitch._spell_pitch_number(13, 'b')
    assert accidental == (abjad.Accidental('ss'), 4)
    accidental = abjad.NamedPitch._spell_pitch_number(13, 'c')
    assert accidental == (abjad.Accidental('s'), 5)
    accidental = abjad.NamedPitch._spell_pitch_number(13, 'd')
    assert accidental == (abjad.Accidental('f'), 5)


def test_pitchtools_NamedPitch__spell_pitch_number_03():

    t = abjad.NamedPitch._spell_pitch_number(14, 'c')
    assert t == (abjad.Accidental('ss'), 5)
    t = abjad.NamedPitch._spell_pitch_number(14, 'd')
    assert t == (abjad.Accidental(''), 5)
    t = abjad.NamedPitch._spell_pitch_number(14, 'e')
    assert t == (abjad.Accidental('ff'), 5)
