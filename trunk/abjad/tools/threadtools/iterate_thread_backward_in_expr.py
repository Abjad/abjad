from abjad.tools.threadtools.component_to_thread_signature import component_to_thread_signature


def iterate_thread_backward_in_expr(expr, klass, thread_signature):
    r'''.. versionadded:: 2.0

    Yield right-to-left instances of `klass` in `expr` with `thread_signature`::

        abjad> from abjad.tools import threadtools

    ::

        abjad> container = Container(Voice(notetools.make_repeated_notes(2)) * 2)
        abjad> container.is_parallel = True
        abjad> container[0].name = 'voice 1'
        abjad> container[1].name = 'vocie 2'
        abjad> staff = Staff(container * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> f(staff)
        \new Staff {
            <<
                \context Voice = "voice 1" {
                    c'8
                    d'8
                }
                \context Voice = "vocie 2" {
                    e'8
                    f'8
                }
            >>
            <<
                \context Voice = "voice 1" {
                    g'8
                    a'8
                }
                \context Voice = "vocie 2" {
                    b'8
                    c''8
                }
            >>
        }

    ::

        abjad> signature = threadtools.component_to_thread_signature(staff[0])
        abjad> for x in threadtools.iterate_thread_backward_in_expr(staff, Note, signature): # doctest: +SKIP
        ...     x
        Note("c''8")
        Note("b'8")
        Note("f'8")
        Note("e'8")

    The important thing to note is that the function yields only those leaves that sit in the same thread.

    Compare with :func:`componenttools.iterate_components_backward_in_expr()
    <abjad.tools.iterate.naive_backward>`.

    .. versionchanged:: 2.0
        renamed ``iterate.thread_backward_in()`` to
        ``threadtools.iterate_thread_backward_in_expr()``.
    '''

    if isinstance(expr, klass) and component_to_thread_signature(expr) == thread_signature:
        yield expr
    if isinstance(expr, (list, tuple)):
        for m in reversed(expr):
            for x in iterate_thread_backward_in_expr(m, klass, thread_signature):
                yield x
    if hasattr(expr, '_music'):
        for m in reversed(expr._music):
            for x in iterate_thread_backward_in_expr(m, klass, thread_signature):
                yield x
