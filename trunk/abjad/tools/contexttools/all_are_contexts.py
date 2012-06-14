from abjad.tools import componenttools


def all_are_contexts(expr):
    '''.. versionadded:: 2.10

    True when `expr` is a sequence of Abjad contexts::

        >>> contexts = 3 * Voice("c'8 d'8 e'8")

    ::

        >>> contexttools.all_are_contexts(contexts)
        True

    True when `expr` is an empty sequence::

        >>> contexttools.all_are_contexts([])
        True

    Otherwise false::

        >>> contexttools.all_are_contexts('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''
    from abjad.tools import contexttools

    return componenttools.all_are_components(expr, klasses=(contexttools.Context,))
