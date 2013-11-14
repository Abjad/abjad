# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_pitchtools_NamedPitch___init___01():
    r'''Initialize by name and octave.
    '''

    pitch = NamedPitch('df', 5)
    assert format(pitch) == "df''"
    assert pitchtools.NamedPitchClass(pitch) == pitchtools.NamedPitchClass('df')
    assert pitch.octave_number == 5
    assert pitchtools.NumberedPitchClass(pitch) == \
        pitchtools.NumberedPitchClass(1)


def test_pitchtools_NamedPitch___init___02():

    npc = pitchtools.NamedPitchClass('cs')
    octave_number = 5
    pitch = NamedPitch(npc, octave_number)
    assert pitch == NamedPitch('cs', 5)


def test_pitchtools_NamedPitch___init___03():
    r'''Initialize by number.
    '''

    pitch = NamedPitch(13)
    assert format(pitch) == "cs''"
    assert pitchtools.NamedPitchClass(pitch) == pitchtools.NamedPitchClass('cs')
    assert pitch.octave_number == 5
    assert pitchtools.NumberedPitchClass(pitch) == \
        pitchtools.NumberedPitchClass(1)


def test_pitchtools_NamedPitch___init___04():
    r'''Initialize by number and diatonic_pitch_class_name.
    '''

    pitch = NamedPitch(13, 'd')

    assert format(pitch) == "df''"
    assert pitchtools.NamedPitchClass(pitch) == \
        pitchtools.NamedPitchClass('df')
    assert pitch.octave_number == 5
    assert pitchtools.NumberedPitchClass(pitch) == \
        pitchtools.NumberedPitchClass(1)


def test_pitchtools_NamedPitch___init___05():
    r'''Initialize by pair.
    '''

    pitch = NamedPitch(('df', 5))

    assert format(pitch) == "df''"
    assert pitchtools.NamedPitchClass(pitch) == \
        pitchtools.NamedPitchClass('df')
    assert pitch.octave_number == 5
    assert pitchtools.NumberedPitchClass(pitch) == \
        pitchtools.NumberedPitchClass(1)


def test_pitchtools_NamedPitch___init___06():

    assert NamedPitch("cs'''") == NamedPitch('cs', 6)
    assert NamedPitch("cs''") == NamedPitch('cs', 5)
    assert NamedPitch("cs'") == NamedPitch('cs', 4)
    assert NamedPitch('cs') == NamedPitch('cs', 3)
    assert NamedPitch('cs,') == NamedPitch('cs', 2)
    assert NamedPitch('cs,,') == NamedPitch('cs', 1)
    assert NamedPitch('cs,,,') == NamedPitch('cs', 0)


def test_pitchtools_NamedPitch___init___07():
    r'''Initialize by reference.
    '''

    pitch_1 = NamedPitch('df', 5)
    pitch = NamedPitch(pitch_1)

    assert format(pitch) == "df''"
    assert pitchtools.NamedPitchClass(pitch) == \
        pitchtools.NamedPitchClass('df')
    assert pitch.octave_number == 5
    assert pitchtools.NumberedPitchClass(pitch) == \
        pitchtools.NumberedPitchClass(1)


def test_pitchtools_NamedPitch___init___08():
    r'''Initialize by pitch-class / octave number string.
    '''

    assert NamedPitch('A4') == NamedPitch("a'")
    assert NamedPitch('C#2') == NamedPitch('cs,')
    assert NamedPitch('D~4') == NamedPitch("dqf'")
    assert NamedPitch('A0') == NamedPitch('a,,,')


def test_pitchtools_NamedPitch___init___09():
    r'''Empty pitches now allowed.
    '''

    assert pytest.raises(Exception, 'NamedPitch()')
