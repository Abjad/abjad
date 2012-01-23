from abjad.tools.componenttools.all_are_components import all_are_components
from abjad.tools.tuplettools.Tuplet import Tuplet


def all_are_tuplets(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad tuplets::

        abjad> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")

    ::

        abjad> tuplettools.all_are_tuplets([tuplet])
        True

    True when `expr` is an empty sequence::

        abjad> tuplettools.all_are_tuplets([])
        True

    Otherwise false::

        abjad> tuplettools.all_are_tuplets('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''

    return all_are_components(expr, klasses=(Tuplet,))
