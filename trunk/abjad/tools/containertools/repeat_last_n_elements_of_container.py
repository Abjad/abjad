# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def repeat_last_n_elements_of_container(container, n=1, total=2):
    r'''Repeats last `n` elements of `container`.

    ..  note:: Deprecated. Use
        container[-n:].copy_and_fracture_crossing_spanners() instead.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> spannertools.BeamSpanner(staff.select_leaves())
        BeamSpanner(c'8, d'8, e'8, f'8)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> containertools.repeat_last_n_elements_of_container(staff, n=2, total=3)
        Staff{8}

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
            e'8 [
            f'8 ]
            e'8 [
            f'8 ]
        }

    Returns `container`.
    '''

    new_components = \
        container[-n:].copy_and_fracture_crossing_spanners(n=total-1)
    container.extend(new_components)
    return container
