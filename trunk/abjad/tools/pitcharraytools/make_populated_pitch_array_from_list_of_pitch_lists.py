def make_populated_pitch_array_from_list_of_pitch_lists(leaf_iterables):
    r'''.. versionadded:: 2.0

    Make populated pitch array from `leaf_iterables`::

        >>> score = Score([])
        >>> score.append(Staff("c'8 d'8 e'8 f'8"))
        >>> score.append(Staff("c'4 d'4"))
        >>> score.append(Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8") * 2))
        >>> f(score)
        \new Score <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
            \new Staff {
                c'4
                d'4
            }
            \new Staff {
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }
            }
        >>

    ::

        >>> array = pitcharraytools.make_populated_pitch_array_from_list_of_pitch_lists(score)
        >>> print array
        [c'     ] [d'     ] [e'     ] [f'     ]
        [c'                   ] [d'                   ]
        [c'] [d'     ] [e'] [c'] [d'     ] [e']

    Return pitch array.
    '''
    from abjad.tools.pitcharraytools.make_pitch_array_from_leaf_iterables import make_pitch_array_from_leaf_iterables

    return make_pitch_array_from_leaf_iterables(leaf_iterables, populate=True)
