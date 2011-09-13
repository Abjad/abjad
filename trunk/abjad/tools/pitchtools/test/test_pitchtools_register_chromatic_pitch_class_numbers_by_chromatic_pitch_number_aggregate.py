from abjad import *


def test_pitchtools_register_chromatic_pitch_class_numbers_by_chromatic_pitch_number_aggregate_01():
    '''Turn pitch-classes into pitches.'''

    pcs = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
    pitches = [10, 19, 20, 23, 24, 26, 27, 29, 30, 33, 37, 40]
    result = pitchtools.register_chromatic_pitch_class_numbers_by_chromatic_pitch_number_aggregate(pcs, pitches)

    assert result == [10, 24, 26, 30, 20, 19, 29, 27, 37, 33, 40, 23]
