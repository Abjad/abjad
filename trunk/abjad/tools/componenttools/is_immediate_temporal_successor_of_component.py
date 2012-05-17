def is_immediate_temporal_successor_of_component(component, expr):
    r'''.. versionadded:: 2.9

    True when `expr` is immediate temporal successor of `component`.

    Otherwise false.
    '''
    from abjad.tools import componenttools

    temporal_successors = []
    cur = component
    while cur is not None:
        next_sibling = componenttools.get_nth_sibling_from_component(cur, 1)
        if next_sibling is None:
            cur = cur.parent
        else:
            temporal_successors = \
                componenttools.get_improper_descendents_of_component_that_start_with_component(next_sibling)
            break

    return expr in temporal_successors
