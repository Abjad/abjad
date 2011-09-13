from abjad import *
import py.test


def test_pitchtools_pentatonic_pitch_number_to_chromatic_pitch_number_01():
    '''Defaults to black keys on the piano.
        Interval sequence 2,3,2,2,3'''

    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(0) == 1
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(1) == 3
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(2) == 6
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(3) == 8
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(4) == 10
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(5) == 13
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(6) == 15
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(-1) == -2
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(-2) == -4


def test_pitchtools_pentatonic_pitch_number_to_chromatic_pitch_number_02():
    '''Pentatonic scale can be transposed.'''

    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(0, 0) == 0
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(1, 0) == 2
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(2, 0) == 5
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(3, 0) == 7
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(4, 0) == 9
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(5, 0) == 12
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(6, 0) == 14
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(-1, 0) == -3
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(-2, 0) == -5

    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(0, -1) == -1
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(1, -1) == 1
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(2, -1) == 4
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(3, -1) == 6
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(4, -1) == 8
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(5, -1) == 11
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(6, -1) == 13
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(-1, -1) == -4
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(-2, -1) == -6


def test_pitchtools_pentatonic_pitch_number_to_chromatic_pitch_number_03():
    '''Pentatonic scale can be rotated.'''

    # Interval sequence 3,2,2,3,2
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(0, 1, 1) == 1
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(1, 1, 1) == 4
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(2, 1, 1) == 6
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(3, 1, 1) == 8
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(4, 1, 1) == 11
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(5, 1, 1) == 13
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(6, 1, 1) == 16
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(-1, 1, 1) == -1
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(-2, 1, 1) == -4

    # Interval sequence 2,2,3,2,3
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(0, 2, 2) == 2
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(1, 2, 2) == 4
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(2, 2, 2) == 6
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(3, 2, 2) == 9
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(4, 2, 2) == 11
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(5, 2, 2) == 14
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(6, 2, 2) == 16
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(-1, 2, 2) == -1
    assert pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(-2, 2, 2) == -3


def test_pitchtools_pentatonic_pitch_number_to_chromatic_pitch_number_04():
    '''Phase must be positive.'''

    assert py.test.raises(AssertionError, 'pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(0, 1, -3)')
