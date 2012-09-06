from abjad.tools import componenttools


def all_are_staves(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad staves::

        >>> staff = Staff("c'4 d'4 e'4 f'4")

    ::

        >>> stafftools.all_are_staves([staff])
        True

    True when `expr` is an empty sequence::

        >>> stafftools.all_are_staves([])
        True

    Otherwise false::

        >>> stafftools.all_are_staves('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''
    from abjad.tools import stafftools

    return componenttools.all_are_components(expr, klasses=(stafftools.Staff,))
