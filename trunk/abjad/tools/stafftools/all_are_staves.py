from abjad.tools.componenttools.all_are_components import all_are_components
from abjad.tools.stafftools.Staff import Staff


def all_are_staves(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad staves::

        abjad> staff = Staff("c'4 d'4 e'4 f'4")

    ::

        abjad> stafftools.all_are_staves([staff])
        True

    True when `expr` is an empty sequence::

        abjad> stafftools.all_are_staves([])
        True

    Otherwise false::

        abjad> stafftools.all_are_staves('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''

    return all_are_components(expr, klasses=(Staff,))
