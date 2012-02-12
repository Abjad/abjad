from abjad.tools.pitchtools.octave_tick_string_to_octave_number import octave_tick_string_to_octave_number
import re


def chromatic_pitch_name_to_octave_number(chromatic_pitch_name):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_name` to octave number::

        abjad> pitchtools.chromatic_pitch_name_to_octave_number('cs')
        3

    Return integer.
    '''

    if not isinstance(chromatic_pitch_name, str):
        raise TypeError('pitch string must be string.')

    match = re.match('^([a-z]+)(\,*|\'*)$', chromatic_pitch_name)
    if match is None:
        raise PitchError('incorrect pitch string format.')

    name, tick_string = match.groups()
    octave_number = octave_tick_string_to_octave_number(tick_string)

    return octave_number
