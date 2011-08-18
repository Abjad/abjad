from abjad.tools.tuplettools.Tuplet import Tuplet


def change_augmented_tuplets_in_expr_to_diminished(tuplet):
    '''.. versionadded:: 2.0

    Multiply the written duration of the leaves in `tuplet`
    by the least power of 2 necessary to diminshed `tuplet`. ::

        abjad> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'8 d'8 e'8")
        abjad> tuplet
        FixedDurationTuplet(1/2, [c'8, d'8, e'8])
        abjad> tuplettools.change_augmented_tuplets_in_expr_to_diminished(tuplet)
        FixedDurationTuplet(1/2, [c'4, d'4, e'4])

    .. todo:: make work with nested tuplets.

    .. versionchanged:: 2.0
        renamed ``tuplettools.augmentation_to_diminution()`` to
        ``tuplettools.change_augmented_tuplets_in_expr_to_diminished()``.
    '''

    if not isinstance(tuplet, Tuplet):
        raise TypeError('must be tuplet.')

    while not tuplet.is_diminution:
        for leaf in tuplet.leaves:
            leaf.written_duration *= 2

    return tuplet
