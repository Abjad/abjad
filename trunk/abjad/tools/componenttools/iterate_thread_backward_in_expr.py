def iterate_thread_backward_in_expr(expr, klass, containment_signature):
    r'''.. versionadded:: 2.0

    .. note: Deprecated. Use `componenttools.iterate_thread_in_expr` instead.

    Yield right-to-left instances of `klass` in `expr` with `containment_signature`::

        >>> container = Container(Voice(notetools.make_repeated_notes(2)) * 2)
        >>> container.is_parallel = True
        >>> container[0].name = 'voice 1'
        >>> container[1].name = 'voice 2'
        >>> staff = Staff(container * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    ::

        >>> f(staff)
        \new Staff {
            <<
                \context Voice = "voice 1" {
                    c'8
                    d'8
                }
                \context Voice = "voice 2" {
                    e'8
                    f'8
                }
            >>
            <<
                \context Voice = "voice 1" {
                    g'8
                    a'8
                }
                \context Voice = "voice 2" {
                    b'8
                    c''8
                }
            >>
        }

    .. note:: Fix function and author example.

    Return generator.

    .. versionchanged:: 2.0
        renamed ``iterate.thread_backward_in()`` to
        ``componenttools.iterate_thread_backward_in_expr()``.

    .. versionchanged:: 2.9
        renamed ``threadtools.iterate_thread_backward_in_expr()`` to
        ``componenttools.iterate_thread_backward_in_expr()``.
    '''
    from abjad.tools import componenttools

    return componenttools.iterate_thread_in_expr(
        expr, klass, containment_signature, reverse=True)
