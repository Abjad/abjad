def component_to_score_index(component):
    r'''.. versionadded:: 2.0

    Change `component` to score index::

        >>> staff_1 = Staff(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 g'8 a'8 }")
        >>> staff_2 = Staff(r"\times 2/3 { b'8 c''8 d''8 }")
        >>> score = Score([staff_1, staff_2])

    ::

        >>> f(score)
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

        >>> for leaf in score.leaves:
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
    parent = cur._parent
    while parent is not None:
        index = parent.index(cur)
        result.insert(0, index)
        cur = parent
        parent = cur._parent
    result = tuple(result)
    return result
