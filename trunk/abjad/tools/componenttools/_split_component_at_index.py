from abjad.tools import durationtools
from abjad.tools.componenttools.get_parent_and_start_stop_indices_of_components import get_parent_and_start_stop_indices_of_components


def _split_component_at_index(component, i, spanners='unfractured'):
    '''General component index split algorithm.
    Works on leaves, tuplets, measures, contexts and unqualified containers.
    Keyword controls spanner behavior at split time.
    Use containertools.split_container_at_index_and_fracture_crossing_spanners() to fracture spanners.
    Use containertools.split_container_at_index_and_do_not_fracture_crossing_spanners() to leave spanners unchanged.
    '''
    from abjad.tools import spannertools
    from abjad.tools import contexttools
    from abjad.tools.leaftools._Leaf import _Leaf
    from abjad.tools.containertools.set_container_multiplier import set_container_multiplier
    from abjad.tools.measuretools.Measure import Measure
    from abjad.tools.tuplettools.Tuplet import Tuplet
    from abjad.tools.tuplettools.FixedDurationTuplet import FixedDurationTuplet

    # convenience leaf index split definition
    if isinstance(component, _Leaf):
        #raise Exception # debug
        if i <= 0:
            if spanners == 'fractured':
                spannertools.fracture_all_spanners_attached_to_component(component, direction = 'left')
            return None, component
        else:
            if spanners == 'fractured':
                spannertools.fracture_all_spanners_attached_to_component(component, direction = 'right')
            return component, None

    # remember container multiplier, if any
    #container_multiplier = getattr(component.duration, 'multiplier', None)
    container_multiplier = getattr(component, 'multiplier', None)

    # partition music of input container
    left_music = component[:i]
    right_music = component[i:]

    # instantiate new left and right containers
    if isinstance(component, Measure):
        meter_denominator = contexttools.get_effective_time_signature(component).denominator
        left_duration = sum([x.prolated_duration for x in left_music])
        left_pair = \
            durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
            left_duration, meter_denominator)
        left_meter = contexttools.TimeSignatureMark(left_pair)
        left = component.__class__(left_meter, left_music)
        right_duration = sum([x.prolated_duration for x in right_music])
        right_pair = \
            durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
            right_duration, meter_denominator)
        right_meter = contexttools.TimeSignatureMark(right_pair)
        right = component.__class__(right_meter, right_music)
    elif isinstance(component, FixedDurationTuplet):
        left = component.__class__(1, left_music)
        right = component.__class__(1, right_music)
        set_container_multiplier(left, container_multiplier)
        set_container_multiplier(right, container_multiplier)
    elif isinstance(component, Tuplet):
        left = component.__class__(container_multiplier, left_music)
        right = component.__class__(container_multiplier, right_music)
    else:
        left = component.__class__(left_music)
        right = component.__class__(right_music)
        set_container_multiplier(left, container_multiplier)
        set_container_multiplier(right, container_multiplier)

    # save left and right halves together for iteration
    halves = [left, right]
    nonempty_halves = [half for half in halves if len(half)]

    # give attached spanners to children
    spannertools.move_spanners_from_component_to_children_of_component(component)

    # incorporate left and right parents in score, if possible
    parent, start, stop = get_parent_and_start_stop_indices_of_components([component])
    if parent is not None:
        # to avoid pychecker slice assignment error
        #parent._music[start:stop+1] = nonempty_halves
        parent._music.__setitem__(slice(start, stop + 1), nonempty_halves)
        for part in nonempty_halves:
            part._parentage._switch(parent)
    else:
        left._parentage._switch(None)
        right._parentage._switch(None)

    # fracture spanners, if requested
    if spanners == 'fractured':
        if len(halves) == 2:
            #left.spanners.fracture(direction = 'right')
            spannertools.fracture_all_spanners_attached_to_component(left, direction = 'right')

    # return new left and right halves
    return left, right
