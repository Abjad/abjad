from abjad.tools.componenttools.all_are_components import all_are_components
from abjad.tools.skiptools.Skip import Skip


def all_are_skips(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad skips::

        abjad> from abjad.tools import skiptools
    
    ::

        abjad> skips = 3 * skiptools.Skip('s4')

    ::

        abjad> skips
        [Skip('s4'), Skip('s4'), Skip('s4')]

    ::

        abjad> skiptools.all_are_skips(skips)
        True

    True when `expr` is an empty sequence::

        abjad> skiptools.all_are_skips([])
        True

    Otherwise false::

        abjad> skiptools.all_are_skips('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''

    return all_are_components(expr, klasses=(Skip,))
