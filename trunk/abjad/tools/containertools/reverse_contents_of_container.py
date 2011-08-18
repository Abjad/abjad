from abjad.tools.containertools.Container import Container


def reverse_contents_of_container(container):
    r'''.. versionadded:: 1.1

    Reverse contents of `container`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> spannertools.BeamSpanner(staff.leaves[:2])
        BeamSpanner(c'8, d'8)
        abjad> spannertools.SlurSpanner(staff.leaves[2:])
        SlurSpanner(e'8, f'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8 ]
            e'8 (
            f'8 )
        }

    ::

        abjad> containertools.reverse_contents_of_container(staff)
        Staff{4}

    ::

        abjad> f(staff) # doctest: +SKIP
        \new Staff {
            f'8 (
            e'8 )
            d'8 [
            c'8 ]
        }

    Return `container`.

    .. versionchanged:: 2.0
        renamed ``containertools.contents_reverse()`` to
        ``containertools.reverse_contents_of_container()``.
    '''
    from abjad.tools import spannertools

    def _offset(x, y):
        if x._offset.start < y._offset.start:
            return -1
        elif y._offset.start < x._offset.start:
            return 1
        else:
            return 0

    if isinstance(container, list):
        container.reverse()
    elif isinstance(container, Container):
        container._music.reverse()
        #spanners = container.spanners.contained
        spanners = spannertools.get_spanners_attached_to_any_improper_child_of_component(container)
        for s in spanners:
            s._components.sort(_offset)

    return container
