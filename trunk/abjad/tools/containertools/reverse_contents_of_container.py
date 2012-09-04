def reverse_contents_of_container(container):
    r'''.. versionadded:: 1.1

    Reverse contents of `container`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beamtools.BeamSpanner(staff.leaves[:2])
        BeamSpanner(c'8, d'8)
        >>> spannertools.SlurSpanner(staff.leaves[2:])
        SlurSpanner(e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8 ]
            e'8 (
            f'8 )
        }

    ::

        >>> containertools.reverse_contents_of_container(staff)
        Staff{4}

    ::

        >>> f(staff) # doctest: +SKIP
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
    from abjad.tools import containertools
    from abjad.tools import spannertools

    def _offset(x, y):
        if x.start_offset < y.start_offset:
            return -1
        elif y.start_offset < x.start_offset:
            return 1
        else:
            return 0

    if isinstance(container, list):
        container.reverse()
    elif isinstance(container, containertools.Container):
        container._music.reverse()
        spanners = spannertools.get_spanners_attached_to_any_improper_child_of_component(container)
        for s in spanners:
            s._components.sort(_offset)

    return container
