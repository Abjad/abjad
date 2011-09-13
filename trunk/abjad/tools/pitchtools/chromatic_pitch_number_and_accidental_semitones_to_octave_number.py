import math


def chromatic_pitch_number_and_accidental_semitones_to_octave_number(
    chromatic_pitch_number, accidental_semitones):
    '''.. versionadded:: 1.1

    Change `chromatic_pitch_number` and `accidental_semitones` to octave number::

        abjad> pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number(12, -2)
        5

    Return integer.

    .. versionchanged:: 2.0
        renamed ``pitchtools.pitch_number_and_accidental_semitones_to_octave()`` to
        ``pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number()``.
    '''

    return int(math.floor((chromatic_pitch_number - accidental_semitones) / 12)) + 4
