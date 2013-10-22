# -*- encoding: utf-8 -*-
# TODO: optimize without multiple full-component traversal.
def iterate_vertical_moments_in_expr(expr, reverse=False):
    r'''Iterate vertical moments forward in `expr`:

    ::

        >>> score = Score([])
        >>> staff = Staff(r"\times 4/3 { d''8 c''8 b'8 }")
        >>> score.append(staff)

    ::

        >>> piano_staff = scoretools.PianoStaff([])
        >>> piano_staff.append(Staff("a'4 g'4"))
        >>> piano_staff.append(Staff(r"""\clef "bass" f'8 e'8 d'8 c'8"""))
        >>> score.append(piano_staff)

    ..  doctest::

        >>> f(score)
        \new Score <<
            \new Staff {
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    d''8
                    c''8
                    b'8
                }
            }
            \new PianoStaff <<
                \new Staff {
                    a'4
                    g'4
                }
                \new Staff {
                    \clef "bass"
                    f'8
                    e'8
                    d'8
                    c'8
                }
            >>
        >>

    ::

        >>> for x in iterationtools.iterate_vertical_moments_in_expr(score):
        ...     x.leaves
        ...
        (Note("d''8"), Note("a'4"), Note("f'8"))
        (Note("d''8"), Note("a'4"), Note("e'8"))
        (Note("c''8"), Note("a'4"), Note("e'8"))
        (Note("c''8"), Note("g'4"), Note("d'8"))
        (Note("b'8"), Note("g'4"), Note("d'8"))
        (Note("b'8"), Note("g'4"), Note("c'8"))

    ::

        >>> for x in iterationtools.iterate_vertical_moments_in_expr(
        ...     piano_staff):
        ...     x.leaves
        ...
        (Note("a'4"), Note("f'8"))
        (Note("a'4"), Note("e'8"))
        (Note("g'4"), Note("d'8"))
        (Note("g'4"), Note("c'8"))

    Iterate vertical moments backward in `expr`:

    ::

    ::

        >>> for x in iterationtools.iterate_vertical_moments_in_expr(
        ...     score, reverse=True):
        ...     x.leaves
        ...
        (Note("b'8"), Note("g'4"), Note("c'8"))
        (Note("b'8"), Note("g'4"), Note("d'8"))
        (Note("c''8"), Note("g'4"), Note("d'8"))
        (Note("c''8"), Note("a'4"), Note("e'8"))
        (Note("d''8"), Note("a'4"), Note("e'8"))
        (Note("d''8"), Note("a'4"), Note("f'8"))

    ::

        >>> for x in iterationtools.iterate_vertical_moments_in_expr(
        ...     piano_staff, reverse=True):
        ...     x.leaves
        ...
        (Note("g'4"), Note("c'8"))
        (Note("g'4"), Note("d'8"))
        (Note("a'4"), Note("e'8"))
        (Note("a'4"), Note("f'8"))

    Returns generator.
    '''
    from abjad.tools import componenttools
    from abjad.tools import containertools
    from abjad.tools import durationtools
    from abjad.tools import iterationtools
    from abjad.tools import selectiontools

    def _buffer_components_starting_with(component, buffer, stop_offsets):
        if not isinstance(component, componenttools.Component):
            raise TypeError
        buffer.append(component)
        stop_offsets.append(component._get_timespan().stop_offset)
        if isinstance(component, containertools.Container):
            if component.is_simultaneous:
                for x in component:
                    _buffer_components_starting_with(x, buffer, stop_offsets)
            else:
                if component:
                    _buffer_components_starting_with(
                        component[0], buffer, stop_offsets)

    def _iterate_vertical_moments_forward_in_expr(expr):
        if not isinstance(expr, componenttools.Component):
            raise TypeError
        governors = (expr, )
        current_offset, stop_offsets, buffer = durationtools.Offset(0), [], []
        _buffer_components_starting_with(expr, buffer, stop_offsets)
        while buffer:
            vertical_moment = selectiontools.VerticalMoment()
            offset = durationtools.Offset(current_offset)
            components = list(buffer)
            components.sort(key=lambda x: x._get_parentage().score_index)
            vertical_moment._offset = offset
            vertical_moment._governors = governors
            vertical_moment._components = components
            yield vertical_moment
            current_offset, stop_offsets = min(stop_offsets), []
            _update_buffer(current_offset, buffer, stop_offsets)

    def _next_in_parent(component):
        if not isinstance(component, componenttools.Component):
            raise TypeError
        selection = component.select(sequential=True)
        parent, start, stop = selection._get_parent_and_start_stop_indices()
        assert start == stop
        if parent is None:
            raise StopIteration
        # can not advance within simultaneous parent
        if parent.is_simultaneous:
            raise StopIteration
        try:
            return parent[start + 1]
        except IndexError:
            raise StopIteration

    def _update_buffer(current_offset, buffer, stop_offsets):
        #print 'At %s with %s ...' % (current_offset, buffer)
        for component in buffer[:]:
            if component._get_timespan().stop_offset <= current_offset:
                buffer.remove(component)
                try:
                    next_component = _next_in_parent(component)
                    _buffer_components_starting_with(
                        next_component, buffer, stop_offsets)
                except StopIteration:
                    pass
            else:
                stop_offsets.append(component._get_timespan().stop_offset)

    if not reverse:
        for x in _iterate_vertical_moments_forward_in_expr(expr):
            yield x
    else:
        moments_in_governor = []
        for component in iterationtools.iterate_components_in_expr(expr):
            offset = component._get_timespan().start_offset
            if offset not in moments_in_governor:
                moments_in_governor.append(offset)
        moments_in_governor.sort()
        for moment_in_governor in reversed(moments_in_governor):
            yield expr._get_vertical_moment_at(moment_in_governor)
