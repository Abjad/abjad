def iterate_timeline_forward_in_expr(expr, klass=None):
    r'''.. versionadded:: 2.0

    .. note: Deprecated. Use `componenttools.iterate_timeline_in_expr` instead.

    Iterate timeline forward in `expr`::

        >>> score = Score([])
        >>> score.append(Staff(notetools.make_repeated_notes(4, Duration(1, 4))))
        >>> score.append(Staff(notetools.make_repeated_notes(4)))
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(score)
        >>> f(score)
        \new Score <<
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }
            \new Staff {
                g'8
                a'8
                b'8
                c''8
            }
        >>
        >>> for leaf in componenttools.iterate_timeline_forward_in_expr(score):
        ...     leaf
        ...
        Note("c'4")
        Note("g'8")
        Note("a'8")
        Note("d'4")
        Note("b'8")
        Note("c''8")
        Note("e'4")
        Note("f'4")

    Iterate leaves when `klass` is none.

    .. todo:: optimize to avoid behind-the-scenes full-score traversal.
    '''
    from abjad.tools import componenttools

    return componenttools.iterate_timeline_in_expr(expr, klass=klass)
