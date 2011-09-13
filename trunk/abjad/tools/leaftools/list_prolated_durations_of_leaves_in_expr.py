from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def list_prolated_durations_of_leaves_in_expr(expr):
    '''.. versionadded:: 2.0

    List prolated durations of leaves in `expr`::

        abjad> staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8") * 2)
        abjad> leaftools.list_prolated_durations_of_leaves_in_expr(staff)
        [Duration(1, 12), Duration(1, 12), Duration(1, 12), Duration(1, 12), Duration(1, 12), Duration(1, 12)]

    Return list of fractions.
    '''

    durations = []

    for leaf in iterate_leaves_forward_in_expr(expr):
        durations.append(leaf.prolated_duration)

    return durations
