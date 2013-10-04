# -*- encoding: utf-8 -*-


def is_alphabetic_accidental_abbreviation(expr):
    '''True when `expr` is an alphabetic accidental abbrevation. Otherwise false:

    ::

        >>> pitchtools.is_alphabetic_accidental_abbreviation('tqs')
        True

    The regex ``^([s]{1,2}|[f]{1,2}|t?q?[fs])!?$`` underlies this predicate.

    Return boolean.
    '''
    from abjad.tools import pitchtools
    if not isinstance(expr, str):
        return False
    return bool(pitchtools.Accidental._alphabetic_accidental_regex.match(expr))
