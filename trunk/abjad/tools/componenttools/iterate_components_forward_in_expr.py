from abjad.tools.componenttools._Component import _Component


def iterate_components_forward_in_expr(expr, klass=_Component, start=0, stop=None):
    r'''.. versionadded:: 1.1

    Iterate components forward in `expr`::

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
        abjad> for x in componenttools.iterate_components_forward_in_expr(staff, Note):
        ...     x
        ...
        Note("c'8")
        Note("d'8")
        Note("e'8")
        Note("f'8")
        Note("g'8")
        Note("a'8")
        Note("b'8")
        Note("c''8")

    .. versionadded:: 2.0
        optional `start` and `stop` keyword parameters.

    ::

        abjad> for x in componenttools.iterate_components_forward_in_expr(staff, Note, start = 0, stop = 4):
        ...     x
        ...
        Note("c'8")
        Note("d'8")
        Note("e'8")
        Note("f'8")

    ::

        abjad> for x in componenttools.iterate_components_forward_in_expr(staff, Note, start = 4):
        ...     x
        ...
        Note("g'8")
        Note("a'8")
        Note("b'8")
        Note("c''8")

    ::

        abjad> for x in componenttools.iterate_components_forward_in_expr(staff, Note, start = 4, stop = 6):
        ...     x
        ...
        Note("g'8")
        Note("a'8")

    This function is thread-agnostic.

    .. versionchanged:: 2.0
        renamed ``iterate.naive()`` to
        ``componenttools.iterate_components_forward_in_expr()``.

    .. versionchanged:: 2.0
        `klass` now defaults to ``_Component``.
    '''

    return _subrange(_forward_generator(expr, klass), start, stop)


def _subrange(iter, start=0, stop=None):
    # if start<0, then 'stop-start' gives a funny result
    # dont have to check stop>=start, as xrange(stop-start) already handles that
    assert 0 <= start

    try:
        # Skip the first few elements, up to 'start' of them:
        for i in xrange(start):
            iter.next()  # no 'yield' to swallow the results

        # Now generate (stop-start) elements (or all elements if stop is None)
        if stop is None:
            for x in iter:
                yield x
        else:
            for i in xrange(stop-start):
                yield iter.next()
    except StopIteration:
        # This happens if we exhaust the list before
        # we generate a total of 'stop' elements
        pass


# Creates a generator that returns elements of type klass,
# descending into containers
def _forward_generator(expr, klass):
    if isinstance(expr, klass):
        yield expr
    if isinstance(expr, (list, tuple)):
        for m in expr:
            for x in _forward_generator(m, klass):
                yield x
    if hasattr(expr, '_music'):
        for m in expr._music:
            for x in _forward_generator(m, klass):
                yield x
