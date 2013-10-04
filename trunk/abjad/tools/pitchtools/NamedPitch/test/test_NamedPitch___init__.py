# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NamedPitch___init___01():
    r'''Init by name and octave.
    '''

    pitch = pitchtools.NamedPitch('df', 5)
    assert pitch.lilypond_format == "df''"
    assert pitch.named_pitch_class == pitchtools.NamedPitchClass('df')
    assert pitch.octave_number == 5
    assert pitch.numbered_pitch_class == pitchtools.NumberedPitchClass(1)


def test_NamedPitch___init___02():

    npc = pitchtools.NamedPitchClass('cs')
    octave_number = 5
    pitch = pitchtools.NamedPitch(npc, octave_number)

    assert pitch == pitchtools.NamedPitch('cs', 5)


def test_NamedPitch___init___03():
    r'''Init by number.
    '''

    pitch = pitchtools.NamedPitch(13)

    assert pitch.lilypond_format == "cs''"
    assert pitch.named_pitch_class == pitchtools.NamedPitchClass('cs')
    assert pitch.octave_number == 5
    assert pitch.numbered_pitch_class == pitchtools.NumberedPitchClass(1)



def test_NamedPitch___init___04():
    r'''Init by number and diatonic_pitch_class_name.
    '''

    pitch = pitchtools.NamedPitch(13, 'd')

    assert pitch.lilypond_format == "df''"
    assert pitch.named_pitch_class == pitchtools.NamedPitchClass('df')
    assert pitch.octave_number == 5
    assert pitch.numbered_pitch_class == pitchtools.NumberedPitchClass(1)



def test_NamedPitch___init___05():
    r'''Init by pair.
    '''

    pitch = pitchtools.NamedPitch(('df', 5))

    assert pitch.lilypond_format == "df''"
    assert pitch.named_pitch_class == pitchtools.NamedPitchClass('df')
    assert pitch.octave_number == 5
    assert pitch.numbered_pitch_class == pitchtools.NumberedPitchClass(1)



def test_NamedPitch___init___06():

    assert pitchtools.NamedPitch("cs'''") == pitchtools.NamedPitch('cs', 6)
    assert pitchtools.NamedPitch("cs''") == pitchtools.NamedPitch('cs', 5)
    assert pitchtools.NamedPitch("cs'") == pitchtools.NamedPitch('cs', 4)
    assert pitchtools.NamedPitch('cs') == pitchtools.NamedPitch('cs', 3)
    assert pitchtools.NamedPitch('cs,') == pitchtools.NamedPitch('cs', 2)
    assert pitchtools.NamedPitch('cs,,') == pitchtools.NamedPitch('cs', 1)
    assert pitchtools.NamedPitch('cs,,,') == pitchtools.NamedPitch('cs', 0)



def test_NamedPitch___init___07():
    r'''Init by reference.
    '''

    pitch_1 = pitchtools.NamedPitch('df', 5)
    pitch = pitchtools.NamedPitch(pitch_1)

    assert pitch.lilypond_format == "df''"
    assert pitch.named_pitch_class == pitchtools.NamedPitchClass('df')
    assert pitch.octave_number == 5
    assert pitch.numbered_pitch_class == pitchtools.NumberedPitchClass(1)


def test_NamedPitch___init___08():
    r'''Init by pitch-class / octave number string.
    '''

    assert pitchtools.NamedPitch('A4') == pitchtools.NamedPitch("a'")
    assert pitchtools.NamedPitch('C#2') == pitchtools.NamedPitch('cs,')
    assert pitchtools.NamedPitch('D~4') == pitchtools.NamedPitch("dqf'")
    assert pitchtools.NamedPitch('A0') == pitchtools.NamedPitch('a,,,')


def test_NamedPitch___init___09():
    r'''Empty pitches now allowed.
    '''

    assert py.test.raises(Exception, 'pitchtools.NamedPitch()')
