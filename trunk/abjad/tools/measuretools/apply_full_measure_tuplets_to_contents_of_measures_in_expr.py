# -*- encoding: utf-8 -*-
import copy
from abjad.tools import mutationtools


def apply_full_measure_tuplets_to_contents_of_measures_in_expr(
    expr, supplement=None):
    r'''Applies full-measure tuplets to contents of measures in `expr`:

    ::

        >>> staff = Staff([
        ...     Measure((2, 8), "c'8 d'8"), 
        ...     Measure((3, 8), "e'8 f'8 g'8")])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \time 3/8
                e'8
                f'8
                g'8
            }
        }

    ::

        >>> measuretools.apply_full_measure_tuplets_to_contents_of_measures_in_expr(staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                {
                    c'8
                    d'8
                }
            }
            {
                \time 3/8
                {
                    e'8
                    f'8
                    g'8
                }
            }
        }

    Returns none.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import selectiontools
    from abjad.tools import tuplettools

    supplement = selectiontools.ContiguousSelection(supplement)
    assert isinstance(supplement, selectiontools.ContiguousSelection)

    for measure in iterationtools.iterate_measures_in_expr(expr):
        target_duration = measure._preprolated_duration
        tuplet = tuplettools.FixedDurationTuplet(target_duration, measure[:])
        if supplement:
            new_supplement = mutationtools.mutate(supplement).copy()
            tuplet.extend(new_supplement)
