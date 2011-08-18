from abjad import *
import py.test


def test_NamedChromaticPitch___init___01():
    '''Init by name and octave.'''

    p = pitchtools.NamedChromaticPitch('df', 5)
    #assert p.numbered_diatonic_pitch == 8
    assert p.format == "df''"
    #assert p.diatonic_pitch_class_name == 'd'
    assert p.named_chromatic_pitch_class == pitchtools.NamedChromaticPitchClass('df')
    #assert p.pitch_number == 13
    assert p.octave_number == 5
    assert p.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(1)


def test_NamedChromaticPitch___init___02():

    npc = pitchtools.NamedChromaticPitchClass('cs')
    octave_number = 5
    pitch = pitchtools.NamedChromaticPitch(npc, octave_number)

    assert pitch == pitchtools.NamedChromaticPitch('cs', 5)


def test_NamedChromaticPitch___init___03():
    '''Init by number.'''

    p = pitchtools.NamedChromaticPitch(13)

    #assert p.numbered_diatonic_pitch == 7
    assert p.format == "cs''"
    #assert p.diatonic_pitch_class_name == 'c'
    assert p.named_chromatic_pitch_class == pitchtools.NamedChromaticPitchClass('cs')
    #assert p.pitch_number == 13
    assert p.octave_number == 5
    assert p.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(1)



def test_NamedChromaticPitch___init___04():
    '''Init by number and diatonic_pitch_class_name.'''

    p = pitchtools.NamedChromaticPitch(13, 'd')

    #assert p.numbered_diatonic_pitch == 8
    assert p.format == "df''"
    #assert p.diatonic_pitch_class_name == 'd'
    assert p.named_chromatic_pitch_class == pitchtools.NamedChromaticPitchClass('df')
    #assert p.pitch_number == 13
    assert p.octave_number == 5
    assert p.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(1)



def test_NamedChromaticPitch___init___05():
    '''Init by pair.'''

    p = pitchtools.NamedChromaticPitch(('df', 5))

    #assert p.numbered_diatonic_pitch == 8
    assert p.format == "df''"
    #assert p.diatonic_pitch_class_name == 'd'
    assert p.named_chromatic_pitch_class == pitchtools.NamedChromaticPitchClass('df')
    #assert p.pitch_number == 13
    assert p.octave_number == 5
    assert p.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(1)



def test_NamedChromaticPitch___init___06():

    assert pitchtools.NamedChromaticPitch("cs'''") == pitchtools.NamedChromaticPitch('cs', 6)
    assert pitchtools.NamedChromaticPitch("cs''") == pitchtools.NamedChromaticPitch('cs', 5)
    assert pitchtools.NamedChromaticPitch("cs'") == pitchtools.NamedChromaticPitch('cs', 4)
    assert pitchtools.NamedChromaticPitch('cs') == pitchtools.NamedChromaticPitch('cs', 3)
    assert pitchtools.NamedChromaticPitch('cs,') == pitchtools.NamedChromaticPitch('cs', 2)
    assert pitchtools.NamedChromaticPitch('cs,,') == pitchtools.NamedChromaticPitch('cs', 1)
    assert pitchtools.NamedChromaticPitch('cs,,,') == pitchtools.NamedChromaticPitch('cs', 0)



def test_NamedChromaticPitch___init___07():
    '''Init by reference.'''

    r = pitchtools.NamedChromaticPitch('df', 5)
    p = pitchtools.NamedChromaticPitch(r)

    #assert p.numbered_diatonic_pitch == 8
    assert p.format == "df''"
    #assert p.diatonic_pitch_class_name == 'd'
    assert p.named_chromatic_pitch_class == pitchtools.NamedChromaticPitchClass('df')
    #assert p.pitch_number == 13
    assert p.octave_number == 5
    assert p.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(1)


def test_NamedChromaticPitch___init___08():
    '''Empty pitches now allowed.
    '''

    assert py.test.raises(Exception, 'pitchtools.NamedChromaticPitch()')

