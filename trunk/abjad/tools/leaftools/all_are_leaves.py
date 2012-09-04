from abjad.tools import componenttools


def all_are_leaves(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad leaves::

        >>> leaves = [Note("c'4"), Rest('r4'), Note("d'4")]

    ::

        >>> leaftools.all_are_leaves(leaves)
        True

    True when `expr` is an empty sequence::

        >>> leaftools.all_are_leaves([])
        True

    Otherwise false::

        >>> leaftools.all_are_leaves('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''
    from abjad.tools import leaftools

    return componenttools.all_are_components(expr, klasses=(leaftools.Leaf,))
