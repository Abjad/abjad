# -*- encoding: utf-8 -*-


def all_are_named_chromatic_pitch_tokens(expr):
    '''True when `expr` is a sequence of named chromatic pitch tokens:

    ::

        >>> named_chromatic_pitch_tokens = [('c', 4), pitchtools.NamedPitch("a'")]

    ::

        >>> pitchtools.all_are_named_chromatic_pitch_tokens(named_chromatic_pitch_tokens)
        True

    True when `expr` is an empty sequence:

    ::

        >>> pitchtools.all_are_named_chromatic_pitch_tokens([])
        True

    Otherwise false:

    ::

        >>> pitchtools.all_are_named_chromatic_pitch_tokens('foo')
        False

    Return boolean.
    '''
    from abjad.tools import pitchtools

    return all(pitchtools.is_named_chromatic_pitch_token(x) for x in expr)
