from abjad.tools.componenttools.all_are_components import all_are_components
from abjad.tools.leaftools._Leaf import _Leaf


def all_are_leaves(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad leaves::

        abjad> leaves = [Note("c'4"), Rest('r4'), Note("d'4")]

    ::

        abjad> leaftools.all_are_leaves(leaves)
        True

    True when `expr` is an empty sequence::

        abjad> leaftools.all_are_leaves([])
        True

    Otherwise false::

        abjad> leaftools.all_are_leaves('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''

    return all_are_components(expr, klasses=(_Leaf,))
