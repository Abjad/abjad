def iterate_thread_forward_in_expr(expr, klass, containment_signature):
    r'''.. versionadded:: 1.1

    Yield left-to-right instances of `klass` in `expr` with `containment_signature`::

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

    ::

        >>> signature = componenttools.component_to_containment_signature(staff.leaves[0])
        >>> for x in componenttools.iterate_thread_forward_in_expr(staff, Note, signature):
        ...     x
        ...
        Note("c'8")
        Note("d'8")
        Note("g'8")
        Note("a'8")

    Return generator.

    .. versionchanged:: 2.0
        renamed ``iterate.thread_forward_in()`` to
        ``componenttools.iterate_thread_forward_in_expr()``.

    .. versionchanged:: 2.9
        renamed ``threadtools.iterate_thread_forward_in_expr()`` to
        ``componenttools.iterate_thread_forward_in_expr()``.
    '''
    from abjad.tools import componenttools

    if isinstance(expr, klass) and \
        componenttools.component_to_containment_signature(expr) == containment_signature:
        yield expr

    if isinstance(expr, (list, tuple)):
        for m in expr:
            for x in componenttools.iterate_thread_forward_in_expr(m, klass, containment_signature):
                yield x

    if hasattr(expr, '_music'):
        for m in expr._music:
            for x in componenttools.iterate_thread_forward_in_expr(m, klass, containment_signature):
                yield x
