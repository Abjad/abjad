from abjad import *


def test_pitchtools_transpose_pitch_carrier_by_melodic_interval_01():

    pitch = pitchtools.NamedChromaticPitch(12)

    diatonic_interval = pitchtools.MelodicDiatonicInterval('minor', 2)
    transposed = pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, diatonic_interval)

    assert transposed == pitchtools.NamedChromaticPitch('df', 5)


def test_pitchtools_transpose_pitch_carrier_by_melodic_interval_02():

    pitch = pitchtools.NamedChromaticPitch(12)

    chromatic_interval = pitchtools.MelodicChromaticInterval(1)
    transposed = pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, chromatic_interval)

    assert transposed == pitchtools.NamedChromaticPitch('cs', 5)


def test_pitchtools_transpose_pitch_carrier_by_melodic_interval_03():
    '''Transpose pitch.'''

    pitch = pitchtools.NamedChromaticPitch(12)
    interval = pitchtools.MelodicChromaticInterval(-3)
    new = pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, interval)
    assert new == pitchtools.NamedChromaticPitch(9)
    assert new is not pitch


def test_pitchtools_transpose_pitch_carrier_by_melodic_interval_04():
    '''Transpose note.'''

    note = Note(12, (1, 4))
    interval = pitchtools.MelodicChromaticInterval(-3)
    new = pitchtools.transpose_pitch_carrier_by_melodic_interval(note, interval)
    assert new.written_pitch == pitchtools.NamedChromaticPitch(9)
    assert new is not note


def test_pitchtools_transpose_pitch_carrier_by_melodic_interval_05():
    '''Transpose chord.'''

    chord = Chord([12, 13, 14], (1, 4))
    interval = pitchtools.MelodicChromaticInterval(-3)
    new = pitchtools.transpose_pitch_carrier_by_melodic_interval(chord, interval)
    assert new.written_pitches == tuple([pitchtools.NamedChromaticPitch(x) for x in [9, 10, 11]])
    assert new is not chord


def test_pitchtools_transpose_pitch_carrier_by_melodic_interval_06():

    pitch = pitchtools.NamedChromaticPitch(12)
    mdi = pitchtools.MelodicDiatonicInterval('minor', -3)

    transposed_pitch = pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, mdi)
    assert transposed_pitch == pitchtools.NamedChromaticPitch('a', 4)


def test_pitchtools_transpose_pitch_carrier_by_melodic_interval_07():
    '''Retun non-pitch-carrying input changed.
    '''

    rest = Rest('r4')

    assert pitchtools.transpose_pitch_carrier_by_melodic_interval(rest, '+m2') is rest
