# -*- encoding: utf-8 -*-


def is_pitch_class_octave_number_string(expr):
    '''True when `expr` is a pitch-class / octave number string. Otherwise false:

    ::

        >>> pitchtools.is_pitch_class_octave_number_string('C#2')
        True

    Quartertone accidentals are supported.

    The regex ``^([A-G])([#]{1,2}|[b]{1,2}|[#]?[+]|[b]?[~]|)([-]?[0-9]+)$``
    underlies this predicate.

    Return boolean.
    '''
    from abjad.tools import pitchtools
    if not isinstance(expr, str):
        return False
    return bool(pitchtools.Pitch._pitch_class_octave_number_regex.match(expr))
