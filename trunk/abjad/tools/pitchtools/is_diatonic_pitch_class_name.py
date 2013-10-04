# -*- encoding: utf-8 -*-


def is_diatonic_pitch_class_name(expr):
    '''True when `expr` is a diatonic pitch-class name. Otherwise false:

    ::

        >>> pitchtools.is_diatonic_pitch_class_name('c')
        True

    The regex ``^[a-g,A-G]$`` underlies this predicate.

    Return boolean.
    '''
    from abjad.tools import pitchtools
    if not isinstance(expr, str):
        return False
    return bool(pitchtools.PitchClass._diatonic_pitch_class_name_regex.match(
        expr))
