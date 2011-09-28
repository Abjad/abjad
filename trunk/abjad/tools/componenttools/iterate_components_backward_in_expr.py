from abjad.tools.componenttools._Component import _Component


def iterate_components_backward_in_expr(expr, klass=_Component, start=0, stop=None):
    r'''.. versionadded:: 1.1

    Iterate components backward in `expr`::

        abjad> staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> f(staff)
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
        abjad> for x in componenttools.iterate_components_backward_in_expr(staff, Note):
        ...     x
        ...
        Note("a'8")
        Note("g'8")
        Note("f'8")
        Note("e'8")
        Note("d'8")
        Note("c'8")

    .. versionadded:: 2.0
        optional `start` and `stop` keyword parameters.

    ::

        abjad> for x in componenttools.iterate_components_backward_in_expr(staff, Note, start = 0, stop = 4):
        ...     x
        ...
        Note("a'8")
        Note("g'8")
        Note("f'8")
        Note("e'8")

    ::

        abjad> for x in componenttools.iterate_components_backward_in_expr(staff, Note, start = 4):
        ...     x
        ...
        Note("d'8")
        Note("c'8")

    ::

        abjad> for x in componenttools.iterate_components_backward_in_expr(staff, Note, start = 4, stop = 6):
        ...     x
        ...
        Note("d'8")
        Note("c'8")

    This function is thread-agnostic.

    .. versionchanged:: 2.0
        renamed ``iterate.backwards()`` to
        ``componenttools.iterate_components_backward_in_expr()``.
    '''

    return _subrange(_backward_generator(expr, klass), start, stop)


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
        # This happens if we exhaust the list before we generate a total of 'stop' elements
        pass


# Creates a generator that returns elements of type klass in reverse order,
# descending into containers
def _backward_generator(expr, klass):
    if isinstance(expr, klass):
        yield expr
    if isinstance(expr, (list, tuple)):
        for m in reversed(expr):
            for x in _backward_generator(m, klass):
                yield x
    if hasattr(expr, '_music'):
        for m in reversed(expr._music):
            for x in _backward_generator(m, klass):
                yield x
