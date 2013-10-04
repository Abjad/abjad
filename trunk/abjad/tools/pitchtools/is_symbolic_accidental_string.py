# -*- encoding: utf-8 -*-


def is_symbolic_accidental_string(expr):
    '''True when `expr` is a symbolic accidental string. Otherwise false:

    ::

        >>> pitchtools.is_symbolic_accidental_string('#+')
        True

    True on empty string.

    The regex ``^([#]{1,2}|[b]{1,2}|[#]?[+]|[b]?[~]|)$`` underlies this 
    predicate.

    Return boolean.
    '''
    from abjad.tools import pitchtools
    if not isinstance(expr, str):
        return False
    return bool(pitchtools.Accidental._symbolic_accidental_string_regex.match(
        expr))
