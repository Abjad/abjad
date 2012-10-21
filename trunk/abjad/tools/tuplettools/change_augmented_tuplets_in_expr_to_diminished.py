# TODO: make work with nested tuplets
def change_augmented_tuplets_in_expr_to_diminished(tuplet):
    '''.. versionadded:: 2.0

    Multiply the written duration of the leaves in `tuplet`
    by the least power of 2 necessary to diminshed `tuplet`::

        >>> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'8 d'8 e'8")

    ::

        >>> tuplet
        FixedDurationTuplet(1/2, [c'8, d'8, e'8])

    ::

        >>> tuplettools.change_augmented_tuplets_in_expr_to_diminished(tuplet)
        FixedDurationTuplet(1/2, [c'4, d'4, e'4])

    .. note:: Does not yet work with nested tuplets.

    Return `tuplet`.
    '''
    from abjad.tools import tuplettools

    if not isinstance(tuplet, tuplettools.Tuplet):
        raise TypeError('must be tuplet.')

    while not tuplet.is_diminution:
        for leaf in tuplet.leaves:
            leaf.written_duration *= 2

    return tuplet
