# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_sort_named_pitch_carriers_in_expr_01():
    r'''Works on notes.
    '''

    chord = Chord([-12, -10, -2, 4, 8, 11, 17, 19, 27, 30, 33, 37], (1, 4))
    sorted_pitches = pitchtools.sort_named_pitch_carriers_in_expr(
        chord.written_pitches)

    sorted_pitch_numbers = [abs(pitchtools.NumberedPitch(pitch))
        for pitch in sorted_pitches]
    sorted_pcs = [pitchtools.NumberedPitchClass(pitch)
        for pitch in sorted_pitches]

    assert sorted_pitch_numbers == [
        -12, 37, -10, 27, 4, 17, 30, 19, 8, 33, -2, 11]
    assert sorted_pcs == [
        pitchtools.NumberedPitchClass(n) for n in 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
