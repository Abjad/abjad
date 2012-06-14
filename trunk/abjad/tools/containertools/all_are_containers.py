from abjad.tools import componenttools


def all_are_containers(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad containers::

        >>> containers = 3 * Container("c'8 d'8 e'8")

    ::

        >>> containertools.all_are_containers(containers)
        True

    True when `expr` is an empty sequence::

        >>> containertools.all_are_containers([])
        True

    Otherwise false::

        >>> containertools.all_are_containers('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''
    from abjad.tools import containertools

    return componenttools.all_are_components(expr, klasses=(containertools.Container,))
