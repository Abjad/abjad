# TODO: make work with nested tuplets
def change_diminished_tuplets_in_expr_to_augmented(tuplet):
    '''.. versionadded:: 2.0

    Divide the written duration of the leaves in `tuplet`
    by the least power of 2 necessary to augment `tuplet`::

        >>> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")

    ::

        >>> tuplet
        FixedDurationTuplet(1/4, [c'8, d'8, e'8])

    ::

        >>> tuplettools.change_diminished_tuplets_in_expr_to_augmented(tuplet)
        FixedDurationTuplet(1/4, [c'16, d'16, e'16])

    .. note:: Does not yet work with nested tuplets.

    Return `tuplet`.
    '''
    from abjad.tools import tuplettools

    if not isinstance(tuplet, tuplettools.Tuplet):
        raise TypeError('must be tuplet')

    while tuplet.is_diminution:
        for leaf in tuplet.leaves:
            leaf.written_duration /= 2

    return tuplet
