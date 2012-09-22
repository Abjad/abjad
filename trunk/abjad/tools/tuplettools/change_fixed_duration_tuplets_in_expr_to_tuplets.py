from abjad.tools import componenttools
from abjad.tools import containertools


def change_fixed_duration_tuplets_in_expr_to_tuplets(expr):
    r'''.. versionadded:: 2.9

    Change fixed-duration tuplets in `expr` to tuplets::

        >>> staff = Staff(2 * tuplettools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8"))

    ::

        >>> staff[:]
        [FixedDurationTuplet(1/4, [c'8, d'8, e'8]), FixedDurationTuplet(1/4, [c'8, d'8, e'8])]

    ::

        >>> tuplettools.change_fixed_duration_tuplets_in_expr_to_tuplets(staff)
        [Tuplet(2/3, [c'8, d'8, e'8]), Tuplet(2/3, [c'8, d'8, e'8])]

    ::

        >>> staff[:]
        [Tuplet(2/3, [c'8, d'8, e'8]), Tuplet(2/3, [c'8, d'8, e'8])]

    Return tuplets.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import tuplettools

    result = []
    for tuplet in iterationtools.iterate_tuplets_in_expr(expr):    
        if isinstance(tuplet, tuplettools.FixedDurationTuplet):
            multiplier = tuplet.multiplier
            new_tuplet = tuplettools.Tuplet(multiplier, [])
            containertools.move_parentage_children_and_spanners_from_components_to_empty_container(
                [tuplet], new_tuplet)
            result.append(new_tuplet)

    return result
