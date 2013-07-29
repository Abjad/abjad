import types
from abjad.tools import selectiontools


def all_are_thread_contiguous_components(
    expr, component_classes=None, allow_orphans=True):
    r'''.. versionadded:: 1.1

    True when elements in `expr` are all thread-contiguous components:

    ::

        >>> container_1 = Container("c'8 d'8")
        >>> inner_voice = Voice("e'8 f'8")
        >>> container_2 = Container("g'8 a'8")
        >>> outer_voice = Voice([container_1, inner_voice, container_2])

    ::

        >>> f(outer_voice)
        \new Voice {
            {
                c'8
                d'8
            }
            \new Voice {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
        }

    ::

        >>> show(outer_voice) # doctest: +SKIP

    ::

        >>> components = [container_1, container_2]
        >>> componenttools.all_are_thread_contiguous_components(components)
        True

    ::

        >>> components = container_1.select_leaves() + container_2.select_leaves()
        >>> componenttools.all_are_thread_contiguous_components(components)
        True

    ::

        >>> components = (container_1, ) + container_2.select_leaves()
        >>> componenttools.all_are_thread_contiguous_components(components)
        True

    ::

        >>> components = [container_1, inner_voice]
        >>> componenttools.all_are_thread_contiguous_components(components)
        False

    Return boolean.
    '''
    from abjad.tools import componenttools

    allowable_types = (
        list,
        tuple,
        types.GeneratorType,
        selectiontools.SequentialSelection,
        )

    if not isinstance(expr, allowable_types):
        return False

    component_classes = component_classes or (componenttools.Component, )
    if not isinstance(component_classes, tuple):
        component_classes = (component_classes, )
    assert isinstance(component_classes, tuple)

    if len(expr) == 0:
        return True

    first = expr[0]
    if not isinstance(first, component_classes):
        return False

    orphan_components = True
    if not first.select_parentage().is_orphan:
        orphan_components = False

    same_thread = True
    thread_proper = True

    first_thread = first.select_parentage().containment_signature
    prev = first
    for cur in expr[1:]:
        if not isinstance(cur, component_classes):
            return False
        if not cur.select_parentage().is_orphan:
            orphan_components = False
        if not cur.select_parentage().containment_signature == first_thread:
            same_thread = False
        if not prev._is_immediate_temporal_successor_of(cur):
            if not _are_thread_proper(prev, cur):
                thread_proper = False
        if (not allow_orphans or 
            (allow_orphans and not orphan_components)) and \
            (not same_thread or not thread_proper):
            return False
        prev = cur

    return True


def _are_thread_proper(component_1, component_2, component_classes=None):
    '''True when

        1. component_1 and component_2 are both Abjad components,
        2. component_1 and component_2 share the same thread,
        3. component_1 precedes component_2 in temporal order, and
        4. there exists no intervening component x that both shares
            the same thread as component_1 and component_2 and
            that intervenes temporally between component_1 and _2.

    Otherwise False.
    '''
    from abjad.tools import componenttools
    from abjad.tools import iterationtools

    if component_classes is None:
        component_classes = (componenttools.Component,)

    # if either input parameter are not Abjad tokens
    if not isinstance(component_1, component_classes) or \
        not isinstance(component_2, component_classes):
        return False

    # if component_1 and component_2 do not share a thread
    first_thread = component_1.select_parentage().containment_signature
    if not first_thread == component_2.select_parentage().containment_signature:
        return False

    # find component_1 offset end time and component_2 offset begin
    first_end = component_1.timespan.stop_offset
    second_begin = component_2.timespan.start_offset

    # if component_1 does not preced component_2
    if not first_end <= second_begin:
        return False

    # if there exists an intervening component of the same thread
    dfs = iterationtools.iterate_components_depth_first(
        component_1, capped=False)
    for node in dfs:
        if node is component_2:
            break
        node_thread = node.select_parentage().containment_signature
        if node_thread == first_thread:
            node_begin = node.timespan.start_offset
            if first_end <= node_begin < second_begin:
                message = 'component %s intervenes between %s and %s.'
                message %= (node, component_1, component_2)
                print message
                return False

    # otherwise, return True
    return True
