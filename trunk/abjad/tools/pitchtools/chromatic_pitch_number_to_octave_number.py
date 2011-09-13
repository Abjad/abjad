import math


def chromatic_pitch_number_to_octave_number(chromatic_pitch_number):
    '''.. versionadded:: 1.1

    Change `chromatic_pitch_number` to octave number::

        abjad> pitchtools.chromatic_pitch_number_to_octave_number(13)
        5

    Return integer.

    .. versionchanged:: 2.0
        renamed ``pitchtools.pitch_number_to_octave()`` to
        ``pitchtools.chromatic_pitch_number_to_octave_number()``.
    '''

    return int(math.floor(chromatic_pitch_number / 12)) + 4
