# -*- encoding: utf-8 -*-


def is_named_interval_quality_abbreviation(expr):
    '''True when `expr` is a named-interval quality abbreviation. Otherwise
    false:

    ::

        >>> pitchtools.is_named_interval_quality_abbreviation('aug')
        True

    The regex ``^M|m|P|aug|dim$`` underlies this predicate.

    Return boolean.
    '''
    from abjad.tools import pitchtools
    if not isinstance(expr, str):
        return False
    return bool(pitchtools.Interval._named_interval_quality_abbreviation_regex.match(expr))
