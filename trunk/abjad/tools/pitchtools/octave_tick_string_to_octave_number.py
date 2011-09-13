import re


def octave_tick_string_to_octave_number(tick_string):
    '''.. versionadded:: 2.0

    Change `tick_string` to octave number::

        abjad> pitchtools.octave_tick_string_to_octave_number("'")
        4

    Raise type error on nonstring input.

    Raise value error on input not of tick string format.

    Return integer.
    '''

    if not isinstance(tick_string, str):
        raise TypeError('tick string must be string.')

    if tick_string == '':
        return 3
    elif re.match("(\\'+)", tick_string):
        return 3 + len(tick_string)
    elif re.match('(\\,+)', tick_string):
        return 3 - len(tick_string)
    else:
        raise ValueError('incorrect tick string format.')
