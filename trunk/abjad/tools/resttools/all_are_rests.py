from abjad.tools.componenttools.all_are_components import all_are_components
from abjad.tools.resttools.Rest import Rest


def all_are_rests(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad rests::

        abjad> rests = [Rest('r4'), Rest('r4'), Rest('r4')]

    ::

        abjad> resttools.all_are_rests(rests)
        True

    True when `expr` is an empty sequence::

        abjad> resttools.all_are_rests([])
        True

    Otherwise false::

        abjad> resttools.all_are_rests('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''

    return all_are_components(expr, klasses=(Rest,))
