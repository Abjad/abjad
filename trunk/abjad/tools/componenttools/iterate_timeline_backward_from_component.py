def iterate_timeline_backward_from_component(expr, klass=None):
    r'''.. versionadded:: 2.0

    .. note: Deprecated. Use `componenttools.iterate_timeline_from_component` instead.

    Iterate timeline backward from `component`::

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
        >>> for leaf in componenttools.iterate_timeline_backward_from_component(score[1][2]):
        ...     leaf
        ...
        Note("b'8")
        Note("c'4")
        Note("a'8")
        Note("g'8")

    Yield components sorted backward by score offset stop time.

    Iterate leaves when `klass` is none.

    .. todo:: optimize to avoid behind-the-scenes full-score traversal.
    '''
    from abjad.tools import componenttools

    return componenttools.iterate_timeline_from_component(
        expr, klass=klass, reverse=True)
