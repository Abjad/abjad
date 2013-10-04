# -*- encoding: utf-8 -*-


def all_are_pitch_class_name_octave_number_pairs(expr):
    '''True when all elements of `expr` are pitch tokens. Otherwise false:

    ::

        >>> pitchtools.all_are_pitch_class_name_octave_number_pairs(
        ... [('c', 4), ('d', 4), pitchtools.NamedPitch('e', 4)])
        True

    Return boolean.
    '''
    from abjad.tools import pitchtools

    if isinstance(expr, (list, tuple, set)):
        if all(pitchtools.is_named_pitch_token(x) for x in expr):
            return True
    return False
