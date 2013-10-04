# -*- encoding: utf-8 -*-


def is_pitch_class_name(expr):
    '''True when `expr` is a chromatic pitch-class name. Otherwise false:

    ::

        >>> pitchtools.is_pitch_class_name('fs')
        True

    The regex ``^([a-g,A-G])(([s]{1,2}|[f]{1,2}|t?q?[fs]|)!?)$`` underlies this
    predicate.

    Return boolean.
    '''
    from abjad.tools import pitchtools
    if not isinstance(expr, str):
        return False
    return bool(pitchtools.PitchClass._pitch_class_name_regex.match(expr))
