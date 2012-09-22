from abjad.tools import componenttools
from abjad.tools import containertools


def change_tuplets_in_expr_to_fixed_duration_tuplets(expr):
    r'''.. versionadded:: 2.9

    Change tuplets in `expr` to fixed-duration tuplets::

        >>> staff = Staff(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { c'8 d'8 e'8 }")

    ::

        >>> staff[:]
        [Tuplet(2/3, [c'8, d'8, e'8]), Tuplet(2/3, [c'8, d'8, e'8])]

    ::

        >>> tuplettools.change_tuplets_in_expr_to_fixed_duration_tuplets(staff)
        [FixedDurationTuplet(1/4, [c'8, d'8, e'8]), FixedDurationTuplet(1/4, [c'8, d'8, e'8])]

    ::

        >>> staff[:]
        [FixedDurationTuplet(1/4, [c'8, d'8, e'8]), FixedDurationTuplet(1/4, [c'8, d'8, e'8])]

    Return tuplets.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import tuplettools

    result = []
    for tuplet in iterationtools.iterate_tuplets_in_expr(expr):    
        if tuplet._class_name == 'Tuplet':
            target_duration = tuplet.preprolated_duration
            new_tuplet = tuplettools.FixedDurationTuplet(target_duration, [])
            containertools.move_parentage_children_and_spanners_from_components_to_empty_container(
                [tuplet], new_tuplet)
            result.append(new_tuplet)

    return result
