def iterate_thread_backward_from_component(component, klass=None):
    r'''.. versionadded:: 2.0

    .. note: Deprecated. Use `componenttools.iterate_thread_from_component` instead.

    Iterate thread backward from `component` and yield instances of `klass`::

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

    Starting from the last leaf in score. ::

        >>> for x in componenttools.iterate_thread_backward_from_component(staff.leaves[-1], Note):
        ...     x
        Note("c''8")
        Note("b'8")
        Note("f'8")
        Note("e'8")

    Yield all components in thread::

        >>> for x in componenttools.iterate_thread_backward_from_component(staff.leaves[-1]):
        ...     x
        Note("c''8")
        Voice-"voice 2"{2}
        Note("b'8")
        Voice-"voice 2"{2}
        Note("f'8")
        Note("e'8")

    Return generator.

    .. versionchanged:: 2.0
        renamed ``iterate.thread_backward_from()`` to
        ``componenttools.iterate_thread_backward_from_component()``.

    .. versionchanged:: 2.9
        renamed ``threadtools.iterate_thread_backward_from_component()`` to
        ``componenttools.iterate_thread_backward_from_component()``.
    '''
    from abjad.tools import componenttools

    return componenttools.iterate_thread_from_component(
        component, klass=klass, reverse=True)
