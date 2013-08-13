# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.selectiontools import mutate


# TODO: trigger this subroutine from a keyword implemented on
#       select(expr).copy_and_fracture_crossing_spanners(climb_parentage=True)
def copy_governed_component_subtree_from_offset_to(
    component, start_offset=0, stop_offset=None):
    r'''Copies governed `component` subtree from `start_offset`
    to `stop_offset`.

    Governed subtree refers to `component` together with the
    children of `component`.

    ..  container:: example

        **Example 1.**

        ::

            >>> voice = Voice(r"c'8 d'8 \times 2/3 { e'8 f'8 g'8 }")
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

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

            >>> new_voice = \
            ...     componenttools.copy_governed_component_subtree_from_offset_to(
            ...     voice, Offset(0, 8), Offset(3, 8))
            >>> show(new_voice) # doctest: +SKIP

        ..  doctest::

            >>> f(new_voice)
            \new Voice {
                c'8
                d'8
                \times 2/3 {
                    e'8
                    f'16
                }
            }

    ..  container:: example

        **Example 2.** Creates ad hoc tuplets as required:

        ::

            >>> voice = Voice([Note("c'4")])
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'4
            }

        ::

            >>> new_voice = \
            ...     componenttools.copy_governed_component_subtree_from_offset_to(
            ...     voice, Offset(0), Offset(1, 12))
            >>> show(new_voice) # doctest: +SKIP

        ..  doctest::

            >>> f(new_voice)
            \new Voice {
                \times 2/3 {
                    c'8
                }
            }

    ..  container:: example

        **Example 3.** Slices tuplets as required:

        ::

            >>> voice = Voice(r"\times 2/3 { c'4 ( d'4 e'4 ) }")
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                \times 2/3 {
                    c'4 (
                    d'4
                    e'4 )
                }
            }

        ::

            >>> new_voice = \
            ...     componenttools.copy_governed_component_subtree_from_offset_to(
            ...     voice[0], Offset(0), Offset(1, 8))
            >>> show(new_voice) # doctest: +SKIP

        ..  doctest::

            >>> f(new_voice)
            \new Voice {
                \times 2/3 {
                    c'8. ( )
                }
            }

    ..  container:: example

        **Example 4.** Does not copy parentage of `component` 
        when `component` is a leaf:

        ::

            >>> voice = Voice(r"\times 2/3 { c'4 ( d'4 e'4 ) }")
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                \times 2/3 {
                    c'4 (
                    d'4
                    e'4 )
                }
            }

        ::

            >>> new_leaf = \
            ... componenttools.copy_governed_component_subtree_from_offset_to(
            ...     voice[0][0], Offset(0), Offset(1, 8))
            >>> new_leaf
            Note("c'8")
            >>> show(new_leaf) # doctest: +SKIP

        ..  doctest::

            >>> f(new_leaf)
            c'8 ( )

    Raises contiguity error when attempting to copy leaves from 
    simultaneous container.

    Returns ``(untrimmed_copy, first_dif, second_dif)`` tuple.
    '''
    from abjad.tools import componenttools
    from abjad.tools import containertools
    from abjad.tools import leaftools

    # check input
    assert isinstance(component, componenttools.Component)
    start_offset = durationtools.Duration(start_offset)
    if start_offset < 0:
        start_offset = durationtools.Duration(0)
    if stop_offset is None:
        stop_offset = component._get_duration()
    else:
        stop_offset = durationtools.Duration(stop_offset)
    assert start_offset <= stop_offset

    # copy component from start offset to stop offset and return
    if isinstance(component, leaftools.Leaf):
        return _copy_leaf_from_start_offset_to_stop_offset(
            component, start_offset, stop_offset)
    #elif isinstance(component, containertools.Container):
    else:
        return _copy_container_from_start_offset_to_stop_offset(
            component, start_offset, stop_offset)
    #else:
    #    raise ValueError('must be leaf or container: {!r}'.format(component))


def _copy_leaf_from_start_offset_to_stop_offset(leaf, start, stop):
    from abjad.tools import leaftools
    if leaf._get_duration() <= start:
        return None
    if leaf._get_duration() < stop:
        stop = leaf._get_duration()
    total = stop - start
    if total == 0:
        return None
    new_leaf = mutate(leaf).copy_and_fracture_crossing_spanners()
    leaftools.set_leaf_duration(new_leaf, total)
    return new_leaf


def _copy_container_from_start_offset_to_stop_offset(container, start, stop):
    from abjad.tools import componenttools
    from abjad.tools import leaftools
    # copy container
    container, first_dif, second_dif = _get_lcopy(container, start, stop)
    # get container start and stop leaves
    leaf_start = container.select_leaves()[0]
    leaf_end = container.select_leaves()[-1]
    # split first leaf
    leaf_start_splitted = componenttools.split_component_at_offset(
        leaf_start, first_dif, fracture_spanners=False)
    assert len(leaf_start_splitted) == 2
    if not leaf_start_splitted[0] == []:
        leaftools.remove_leaf_and_shrink_durated_parent_containers(
            leaf_start_splitted[0][0])
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
    for i, leaf in enumerate(
        iterationtools.iterate_leaves_in_expr(container)):
        total_dur += leaf._get_duration()
        if total_dur == start and start_leaf is None:
            start_leaf = i
            first_dif = 0
        elif start < total_dur and start_leaf is None:
            start_leaf = i
            first_dif = leaf._get_duration() - (total_dur - start)
            #print first_dif
        if stop <= total_dur and stop_leaf is None:
            stop_leaf = i + 1
            #second_dif = leaf._get_duration() - (total_dur - stop)
            remaining_duration = total_dur - stop
            if remaining_duration != 0:
                second_dif = leaf._get_duration() - remaining_duration
            #print second_dif
            #print 'breaking after stop'
            break
    #print start_leaf, stop_leaf
    untrimmed_copy = \
        componenttools.copy_governed_component_subtree_by_leaf_range(
        container, start_leaf, stop_leaf)
    return untrimmed_copy, first_dif, second_dif
