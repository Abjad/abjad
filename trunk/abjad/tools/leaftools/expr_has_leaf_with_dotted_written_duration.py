from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def expr_has_leaf_with_dotted_written_duration(expr):
    '''.. versionadded:: 2.0

    True when `expr` has at least one leaf with dotted writtern duration::

        abjad> notes = notetools.make_notes([0], [(1, 16), (2, 16), (3, 16)])
        abjad> leaftools.expr_has_leaf_with_dotted_written_duration(notes)
        True

    False otherwise::

        abjad> notes = notetools.make_notes([0], [(1, 16), (2, 16), (4, 16)])
        abjad> leaftools.expr_has_leaf_with_dotted_written_duration(notes)
        False

    Return boolean.
    '''

    for leaf in iterate_leaves_forward_in_expr(expr):
        if not leaf.written_duration._numerator == 1:
            return True
    return False
