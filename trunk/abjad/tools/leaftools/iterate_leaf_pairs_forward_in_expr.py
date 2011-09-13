from abjad.tools import sequencetools


def iterate_leaf_pairs_forward_in_expr(expr):
    r'''.. versionadded:: 2.0

    Iterate leaf pairs forward in `expr`::

        abjad> score = Score([])
        abjad> notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"), Note("g'4")]
        abjad> score.append(Staff(notes))
        abjad> notes = [Note(x, (1, 4)) for x in [-12, -15, -17]]
        abjad> score.append(Staff(notes))
        abjad> contexttools.ClefMark('bass')(score[1])
        ClefMark('bass')(Staff{3})

    ::

        abjad> f(score)
        \new Score <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
                g'4
            }
            \new Staff {
                \clef "bass"
                c4
                a,4
                g,4
            }
        >>

    ::

        abjad> for pair in leaftools.iterate_leaf_pairs_forward_in_expr(score):
        ...        pair
        (Note("c'8"), Note('c4'))
        (Note("c'8"), Note("d'8"))
        (Note('c4'), Note("d'8"))
        (Note("d'8"), Note("e'8"))
        (Note("d'8"), Note('a,4'))
        (Note('c4'), Note("e'8"))
        (Note('c4'), Note('a,4'))
        (Note("e'8"), Note('a,4'))
        (Note("e'8"), Note("f'8"))
        (Note('a,4'), Note("f'8"))
        (Note("f'8"), Note("g'4"))
        (Note("f'8"), Note('g,4'))
        (Note('a,4'), Note("g'4"))
        (Note('a,4'), Note('g,4'))
        (Note("g'4"), Note('g,4'))

    Iterate leaf pairs left-to-right and top-to-bottom.

    Return generator.
    '''
    from abjad.tools.verticalitytools.iterate_vertical_moments_forward_in_expr import iterate_vertical_moments_forward_in_expr

    vertical_moments = iterate_vertical_moments_forward_in_expr(expr)
    for moment_1, moment_2 in sequencetools.iterate_sequence_pairwise_strict(vertical_moments):
        for pair in sequencetools.yield_all_unordered_pairs_of_sequence(moment_1.start_leaves):
            yield pair
        pairs = sequencetools.yield_all_pairs_between_sequences(moment_1.leaves, moment_2.start_leaves)
        for pair in pairs:
            yield pair
    else:
        for pair in sequencetools.yield_all_unordered_pairs_of_sequence(moment_2.start_leaves):
            yield pair
