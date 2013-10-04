# -*- encoding: utf-8 -*-


def is_pitch_name(expr):
    '''True `expr` is a chromatic pitch name. Otherwise false:

    ::

        >>> pitchtools.is_pitch_name('c,')
        True

    The regex ``^([a-g,A-G])(([s]{1,2}|[f]{1,2}|t?q?[f,s]|)!?)(,+|'+|)$`` underlies this predicate.

    Return boolean.
    '''
    from abjad.tools import pitchtools
    if not isinstance(expr, str):
        return False
    return bool(pitchtools.Pitch._pitch_name_regex.match(expr))
