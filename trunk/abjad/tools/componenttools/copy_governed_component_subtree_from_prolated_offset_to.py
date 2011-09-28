from abjad.tools.componenttools._Component import _Component
from abjad.tools import durationtools


def copy_governed_component_subtree_from_prolated_offset_to(component, start=0, stop=None):
    r'''.. versionadded:: 1.1

    Clone governed `component` subtree from `start` prolated duration
    to `stop` prolated duration.

    Governed subtree refers to `component` together with the children of `component`::

        abjad> voice = Voice(notetools.make_repeated_notes(2))
        abjad> voice.append(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)))
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(voice)
        abjad> f(voice)
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

        abjad> new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(voice, (0, 8), (3, 8))
        abjad> f(new)
        \new Voice {
           c'8
           d'8
           \times 2/3 {
              e'8
              f'16
           }
        }

    Raise contiguity error if asked to slice a parallel container. ::

        abjad> staff = Staff(Voice("c'8 d'8") * 2)
        abjad> staff.is_parallel = True
        abjad> f(staff)
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

        abjad> new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(voice, (0, 8), (1, 8))
        abjad> f(new)
        \new Voice {
            c'8
        }

    Cases with ``0 < start`` do not work correctly::

        abjad> new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(voice, (1, 8), (2, 8))
        abjad> f(new)
        \new Voice {
            c'8
            d'8
        }

    Create ad hoc tuplets as required::

        abjad> voice = Voice([Note("c'4")])
        abjad> new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(voice, 0, (1, 12))
        abjad> f(new)
        \new Voice {
            \times 2/3 {
                c'8
            }
        }

    Function does NOT clone parentage of `component` when `component` is a leaf::

        abjad> voice = Voice([Note("c'4")])
        abjad> new_leaf = componenttools.copy_governed_component_subtree_from_prolated_offset_to(voice[0], 0, (1, 8))
        abjad> f(new_leaf)
        c'8
        abjad> new_leaf._parentage.parent is None
        True

    Return (untrimmed_copy, first_dif, second_dif).

    .. versionchanged:: 2.0
        renamed ``componenttools.clone_governed_component_subtree_from_prolated_duration_to()`` to
        ``componenttools.copy_governed_component_subtree_from_prolated_offset_to()``.
    '''
    from abjad.tools.leaftools._Leaf import _Leaf
    from abjad.tools.containertools.Container import Container
    assert isinstance(component, _Component)
    start = durationtools.Duration(*durationtools.duration_token_to_duration_pair(start))
    if start < 0:
        start = durationtools.Duration(0)
    if stop is None:
        stop = component.prolated_duration
    else:
        stop = durationtools.Duration(*durationtools.duration_token_to_duration_pair(stop))
    assert start <= stop
    if isinstance(component, _Leaf):
        return _scopy_leaf(component, start, stop)
    elif isinstance(component, Container):
        return _scopy_container(component, start, stop)
    else:
        raise ValueError('must be leaf or container.')


def _scopy_leaf(leaf, start, stop):
    from abjad.tools import leaftools
    from abjad.tools.componenttools.copy_components_and_fracture_crossing_spanners import copy_components_and_fracture_crossing_spanners
    if leaf.prolated_duration <= start:
        return None
    if leaf.prolated_duration < stop:
        stop = leaf.prolated_duration
    total = stop - start
    if total == 0:
        return None
    new = copy_components_and_fracture_crossing_spanners([leaf])[0]
    leaftools.set_preprolated_leaf_duration(new, total)
    return new


def _scopy_container(container, start, stop):
    from abjad.tools import leaftools
    from abjad.tools.componenttools.split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners import split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners
    container, first_dif, second_dif = _get_lcopy(container, start, stop)
    #print first_dif, second_dif
    leaf_start = container.leaves[0]
    leaf_end = container.leaves[-1]
    # split first leaf
    leaf_start_splitted = split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners(leaf_start, first_dif)
    if len(leaf_start_splitted) == 2:
        leaftools.remove_leaf_and_shrink_durated_parent_containers(
            leaf_start_splitted[0][0])
    # split second leaf
    leaf_end_splitted = split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners(leaf_end, second_dif)
    if len(leaf_end_splitted) == 2:
        leaftools.remove_leaf_and_shrink_durated_parent_containers(
            leaf_end_splitted[1][0])
    return container


def _get_lcopy(container, start, stop):
    from abjad.tools.componenttools.copy_governed_component_subtree_by_leaf_range import copy_governed_component_subtree_by_leaf_range
    from abjad.tools import leaftools
    total_dur = durationtools.Duration(0)
    start_leaf, stop_leaf = None, None
    first_dif = second_dif = 0
    for i, leaf in enumerate(leaftools.iterate_leaves_forward_in_expr(container)):
        total_dur += leaf.prolated_duration
        if total_dur == start and start_leaf is None:
            start_leaf = i
            first_dif = 0
        elif start < total_dur and start_leaf is None:
            start_leaf = i
            first_dif = leaf.prolated_duration - (total_dur - start)
            #print first_dif
        if stop <= total_dur and stop_leaf is None:
            stop_leaf = i + 1
            #second_dif = leaf.prolated_duration - (total_dur - stop)
            flamingo = total_dur - stop
            if flamingo != 0:
                second_dif = leaf.prolated_duration - flamingo
            #print second_dif
            #print 'breaking after stop'
            break
    #print start_leaf, stop_leaf
    untrimmed_copy = copy_governed_component_subtree_by_leaf_range(
        container, start_leaf, stop_leaf)
    return untrimmed_copy, first_dif, second_dif
