from abjad import *


def test_pitchtools_ordered_chromatic_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers_01():
    '''True when all pcs appear in octave order in pitches.'''

    pcs = [2, 7, 10]
    pitches = [6, 9, 12, 13, 14, 19, 22, 27, 28, 29, 32, 35]
    assert pitchtools.ordered_chromatic_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers(pcs, pitches)


def test_pitchtools_ordered_chromatic_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers_02():
    '''True when all pcs appear in octave order in pitches.'''

    pcs = [2, 3, 4]
    pitches = [6, 9, 12, 13, 14, 19, 22, 27, 28, 29, 32, 35]
    assert not pitchtools.ordered_chromatic_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers(pcs, pitches)
