from abjad.tools.componenttools.all_are_components import all_are_components
from abjad.tools.measuretools.Measure import Measure


def all_are_measures(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad measures::

        >>> measures = 3 * Measure((3, 4), "c'4 d'4 e'4")

    ::

        >>> measures
        [Measure(3/4, [c'4, d'4, e'4]), Measure(3/4, [c'4, d'4, e'4]), Measure(3/4, [c'4, d'4, e'4])]

    ::

        >>> measuretools.all_are_measures(measures)
        True

    True when `expr` is an empty sequence::

        >>> measuretools.all_are_measures([])
        True

    Otherwise false::

        >>> measuretools.all_are_measures('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''

    return all_are_components(expr, klasses=(Measure,))
