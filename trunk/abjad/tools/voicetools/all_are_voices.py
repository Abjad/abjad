from abjad.tools import componenttools


def all_are_voices(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad voices::

        >>> voice = Voice("c'4 d'4 e'4 f'4")

    ::

        >>> voicetools.all_are_voices([voice])
        True

    True when `expr` is an empty sequence::

        >>> voicetools.all_are_voices([])
        True

    Otherwise false::

        >>> voicetools.all_are_voices('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''

    from abjad.tools import voicetools

    return componenttools.all_are_components(expr, klasses=(voicetools.Voice,))
