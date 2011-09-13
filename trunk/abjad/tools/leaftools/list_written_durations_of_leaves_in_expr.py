from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def list_written_durations_of_leaves_in_expr(expr):
    '''.. versionadded:: 2.0

    List the written durations of leaves in `expr`::

        abjad> staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8") * 2)
        abjad> leaftools.list_written_durations_of_leaves_in_expr(staff)
        [Duration(1, 8), Duration(1, 8), Duration(1, 8), Duration(1, 8), Duration(1, 8), Duration(1, 8)]

    Return list of fractions.
    '''

    durations = []

    for leaf in iterate_leaves_forward_in_expr(expr):
        durations.append(leaf.written_duration)

    return durations
