# -*- encoding: utf-8 -*-
def reverse_contents_of_container(container):
    r'''Reverse contents of `container`:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> spannertools.BeamSpanner(staff.select_leaves()[:2])
        BeamSpanner(c'8, d'8)
        >>> spannertools.SlurSpanner(staff.select_leaves()[2:])
        SlurSpanner(e'8, f'8)

    ..  doctest::

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

    ..  doctest::

        >>> f(staff) # doctest: +SKIP
        \new Staff {
            f'8 (
            e'8 )
            d'8 [
            c'8 ]
        }

    Return `container`.
    '''
    from abjad.tools import containertools
    from abjad.tools import spannertools

    def _offset(x, y):
        if x.get_timespan().start_offset < y.get_timespan().start_offset:
            return -1
        elif y.get_timespan().start_offset < x.get_timespan().start_offset:
            return 1
        else:
            return 0

    if isinstance(container, list):
        container.reverse()
    elif isinstance(container, containertools.Container):
        container._music.reverse()
        container._mark_entire_score_tree_for_later_update('prolated')
        spanners = spannertools.get_spanners_attached_to_any_improper_child_of_component(
            container)
        for s in spanners:
            s._components.sort(_offset)

    return container
