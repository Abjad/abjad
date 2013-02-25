from abjad.tools import durationtools


def copy_governed_component_subtree_from_offset_to(component, start=0, stop=None):
    r'''.. versionadded:: 1.1

    Copy governed `component` subtree from `start` prolated duration
    to `stop` prolated duration.

    Governed subtree refers to `component` together with the
    children of `component`::

        >>> voice = Voice(r"c'8 d'8 \times 2/3 { e'8 f'8 g'8 }")

    ::

        >>> f(voice)
        \new Voice {
           c'8
           d'8
           \times 2/3 {
              e'8
              f'8
              g'8
           }
        }

    ::

        >>> new = componenttools.copy_governed_component_subtree_from_offset_to(
        ...     voice, (0, 8), (3, 8))

    ::

        >>> f(new)
        \new Voice {
           c'8
           d'8
           \times 2/3 {
              e'8
              f'16
           }
        }

    Raise contiguity error if asked to slice a parallel container. ::

        >>> staff = Staff(Voice("c'8 d'8") * 2)
        >>> staff.is_parallel = True
        >>> f(staff)
        \new Staff <<
        \new Voice {
            c'8
            d'8
        }
        \new Voice {
            c'8
            d'8
        }
        >>

    Raise contiguity error when attempting to copy fleaves from parallel container.

    But note that cases with ``0 = start`` work correctly::

        >>> new = componenttools.copy_governed_component_subtree_from_offset_to(
        ...     voice, (0, 8), (1, 8))

    ::

        >>> f(new)
        \new Voice {
            c'8
        }

    Cases with ``0 < start`` do not work correctly::

        >>> new = componenttools.copy_governed_component_subtree_from_offset_to(
        ...     voice, (1, 8), (2, 8))

    ::

        >>> f(new)
        \new Voice {
            c'8
            d'8
        }

    Create ad hoc tuplets as required::

        >>> voice = Voice([Note("c'4")])
        >>> new = componenttools.copy_governed_component_subtree_from_offset_to(
        ...     voice, 0, (1, 12))

    ::

        >>> f(new)
        \new Voice {
            \times 2/3 {
                c'8
            }
        }

    Function does NOT copy parentage of `component` when `component` is a leaf::

        >>> voice = Voice([Note("c'4")])
        >>> new_leaf = componenttools.copy_governed_component_subtree_from_offset_to(
        ...     voice[0], 0, (1, 8))

    ::

        >>> f(new_leaf)
        c'8

    ::

        >>> new_leaf.parent is None
        True

    Return ``(untrimmed_copy, first_dif, second_dif)``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import containertools
    from abjad.tools import leaftools

    # check input
    assert isinstance(component, componenttools.Component)
    start = durationtools.Duration(start)
    if start < 0:
        start = durationtools.Duration(0)
    if stop is None:
        stop = component.duration
    else:
        stop = durationtools.Duration(stop)
    assert start <= stop

    # copy component from start offset to stop offset and return
    if isinstance(component, leaftools.Leaf):
        return _copy_leaf_from_start_offset_to_stop_offset(component, start, stop)
    elif isinstance(component, containertools.Container):
        return _copy_container_from_start_offset_to_stop_offset(component, start, stop)
    else:
        raise ValueError('must be leaf or container: {!r}'.format(component))


def _copy_leaf_from_start_offset_to_stop_offset(leaf, start, stop):
    from abjad.tools import componenttools
    from abjad.tools import leaftools

    if leaf.duration <= start:
        return None

    if leaf.duration < stop:
        stop = leaf.duration

    total = stop - start
    if total == 0:
        return None

    new_leaf = componenttools.copy_components_and_fracture_crossing_spanners([leaf])[0]
    leaftools.set_preprolated_leaf_duration(new_leaf, total)

    return new_leaf


def _copy_container_from_start_offset_to_stop_offset(container, start, stop):
    from abjad.tools import componenttools
    from abjad.tools import leaftools

    # copy container
    container, first_dif, second_dif = _get_lcopy(container, start, stop)

    # get container start and stop leaves
    leaf_start = container.leaves[0]
    leaf_end = container.leaves[-1]

    # split first leaf
    leaf_start_splitted = componenttools.split_component_at_offset(
        leaf_start, first_dif, fracture_spanners=False)
    assert len(leaf_start_splitted) == 2
    if not leaf_start_splitted[0] == []:
        leaftools.remove_leaf_and_shrink_durated_parent_containers(leaf_start_splitted[0][0])

    # split second leaf
    leaf_end_splitted = componenttools.split_component_at_offset(
        leaf_end, second_dif, fracture_spanners=False)
    assert len(leaf_end_splitted) == 2
    if not leaf_end_splitted[0] == []:
        leaftools.remove_leaf_and_shrink_durated_parent_containers(
            leaf_end_splitted[1][0])

    # return adjusted container
    return container


# TODO: rename explicitly
def _get_lcopy(container, start, stop):
    from abjad.tools import componenttools
    from abjad.tools import iterationtools

    # initialize loop variables
    total_dur = durationtools.Duration(0)
    start_leaf, stop_leaf = None, None
    first_dif = second_dif = 0

    for i, leaf in enumerate(iterationtools.iterate_leaves_in_expr(container)):
        total_dur += leaf.duration
        if total_dur == start and start_leaf is None:
            start_leaf = i
            first_dif = 0
        elif start < total_dur and start_leaf is None:
            start_leaf = i
            first_dif = leaf.duration - (total_dur - start)
            #print first_dif
        if stop <= total_dur and stop_leaf is None:
            stop_leaf = i + 1
            #second_dif = leaf.duration - (total_dur - stop)
            flamingo = total_dur - stop
            if flamingo != 0:
                second_dif = leaf.duration - flamingo
            #print second_dif
            #print 'breaking after stop'
            break

    #print start_leaf, stop_leaf
    untrimmed_copy = componenttools.copy_governed_component_subtree_by_leaf_range(
        container, start_leaf, stop_leaf)

    return untrimmed_copy, first_dif, second_dif
