# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NamedChromaticPitch___init___01():
    r'''Init by name and octave.
    '''

    pitch = pitchtools.NamedChromaticPitch('df', 5)
    assert pitch.lilypond_format == "df''"
    assert pitch.named_chromatic_pitch_class == pitchtools.NamedChromaticPitchClass('df')
    assert pitch.octave_number == 5
    assert pitch.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(1)


def test_NamedChromaticPitch___init___02():

    npc = pitchtools.NamedChromaticPitchClass('cs')
    octave_number = 5
    pitch = pitchtools.NamedChromaticPitch(npc, octave_number)

    assert pitch == pitchtools.NamedChromaticPitch('cs', 5)


def test_NamedChromaticPitch___init___03():
    r'''Init by number.
    '''

    pitch = pitchtools.NamedChromaticPitch(13)

    assert pitch.lilypond_format == "cs''"
    assert pitch.named_chromatic_pitch_class == pitchtools.NamedChromaticPitchClass('cs')
    assert pitch.octave_number == 5
    assert pitch.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(1)



def test_NamedChromaticPitch___init___04():
    r'''Init by number and diatonic_pitch_class_name.
    '''

    pitch = pitchtools.NamedChromaticPitch(13, 'd')

    assert pitch.lilypond_format == "df''"
    assert pitch.named_chromatic_pitch_class == pitchtools.NamedChromaticPitchClass('df')
    assert pitch.octave_number == 5
    assert pitch.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(1)



def test_NamedChromaticPitch___init___05():
    r'''Init by pair.
    '''

    pitch = pitchtools.NamedChromaticPitch(('df', 5))

    assert pitch.lilypond_format == "df''"
    assert pitch.named_chromatic_pitch_class == pitchtools.NamedChromaticPitchClass('df')
    assert pitch.octave_number == 5
    assert pitch.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(1)



def test_NamedChromaticPitch___init___06():

    assert pitchtools.NamedChromaticPitch("cs'''") == pitchtools.NamedChromaticPitch('cs', 6)
    assert pitchtools.NamedChromaticPitch("cs''") == pitchtools.NamedChromaticPitch('cs', 5)
    assert pitchtools.NamedChromaticPitch("cs'") == pitchtools.NamedChromaticPitch('cs', 4)
    assert pitchtools.NamedChromaticPitch('cs') == pitchtools.NamedChromaticPitch('cs', 3)
    assert pitchtools.NamedChromaticPitch('cs,') == pitchtools.NamedChromaticPitch('cs', 2)
    assert pitchtools.NamedChromaticPitch('cs,,') == pitchtools.NamedChromaticPitch('cs', 1)
    assert pitchtools.NamedChromaticPitch('cs,,,') == pitchtools.NamedChromaticPitch('cs', 0)



def test_NamedChromaticPitch___init___07():
    r'''Init by reference.
    '''

    pitch_1 = pitchtools.NamedChromaticPitch('df', 5)
    pitch = pitchtools.NamedChromaticPitch(pitch_1)

    assert pitch.lilypond_format == "df''"
    assert pitch.named_chromatic_pitch_class == pitchtools.NamedChromaticPitchClass('df')
    assert pitch.octave_number == 5
    assert pitch.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(1)


def test_NamedChromaticPitch___init___08():
    r'''Init by pitch-class / octave number string.
    '''

    assert pitchtools.NamedChromaticPitch('A4') == pitchtools.NamedChromaticPitch("a'")
    assert pitchtools.NamedChromaticPitch('C#2') == pitchtools.NamedChromaticPitch('cs,')
    assert pitchtools.NamedChromaticPitch('D~4') == pitchtools.NamedChromaticPitch("dqf'")
    assert pitchtools.NamedChromaticPitch('A0') == pitchtools.NamedChromaticPitch('a,,,')


def test_NamedChromaticPitch___init___09():
    r'''Empty pitches now allowed.
    '''

    assert py.test.raises(Exception, 'pitchtools.NamedChromaticPitch()')
