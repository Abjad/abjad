from abjad.tools import componenttools


def all_are_tuplets(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad tuplets::

        >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")

    ::

        >>> tuplettools.all_are_tuplets([tuplet])
        True

    True when `expr` is an empty sequence::

        >>> tuplettools.all_are_tuplets([])
        True

    Otherwise false::

        >>> tuplettools.all_are_tuplets('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''
    from abjad.tools import tuplettools

    return componenttools.all_are_components(expr, klasses=(tuplettools.Tuplet,))
