def component_to_score_index(component):
    r'''.. versionadded:: 2.0

    Change `component` to score index::

        abjad> staff_1 = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
        abjad> staff_2 = Staff([tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3))])
        abjad> score = Score([staff_1, staff_2])
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(score)
        abjad> f(score)
        \new Score <<
            \new Staff {
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }
                \times 2/3 {
                    f'8
                    g'8
                    a'8
                }
            }
            \new Staff {
                \times 2/3 {
                    b'8
                    c''8
                    d''8
                }
            }
        >>

    ::

        abjad> for leaf in score.leaves:
        ...     leaf, componenttools.component_to_score_index(leaf)
        ...
        (Note("c'8"), (0, 0, 0))
        (Note("d'8"), (0, 0, 1))
        (Note("e'8"), (0, 0, 2))
        (Note("f'8"), (0, 1, 0))
        (Note("g'8"), (0, 1, 1))
        (Note("a'8"), (0, 1, 2))
        (Note("b'8"), (1, 0, 0))
        (Note("c''8"), (1, 0, 1))
        (Note("d''8"), (1, 0, 2))

    Return tuple of zero or more nonnegative integers.
    '''

    result = []
    cur = component
    parent = cur._parentage.parent
    while parent is not None:
        index = parent.index(cur)
        result.insert(0, index)
        cur = parent
        parent = cur._parentage.parent
    result = tuple(result)
    return result
