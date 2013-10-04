# -*- encoding: utf-8 -*-
import math


def pitch_number_and_accidental_semitones_to_octave_number(
    pitch_number, accidental_semitones):
    '''Change `pitch_number` and `accidental_semitones` to octave number:

    ::

        >>> pitchtools.pitch_number_and_accidental_semitones_to_octave_number(12, -2)
        5

    Return integer.
    '''

    return int(math.floor((pitch_number - accidental_semitones) / 12)) + 4
