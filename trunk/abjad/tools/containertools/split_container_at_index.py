from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import leaftools


def split_container_at_index(component, i, fracture_spanners=False):
    r'''.. versionadded:: 1.1

    General component index split algorithm.
    Works on leaves, tuplets, measures, contexts and unqualified containers.
    Keyword controls spanner behavior at split time.
    Use containertools.split_container_at_index_and_fracture_crossing_spanners() 
    to fracture spanners.
    Use containertools.split_container_at_index_and_do_not_fracture_crossing_spanners() 
    to leave spanners unchanged.

    Example 1. Split container and do not fracture crossing spanners::

        >>> voice = Voice(Measure((3, 8), "c'8 c'8 c'8") * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
        >>> beam = beamtools.BeamSpanner(voice[:])

    ::

        >>> f(voice)
        \new Voice {
            {
                \time 3/8
                c'8 [
                d'8
                e'8
            }
            {
                f'8
                g'8
                a'8 ]
            }
        }

    ::

        >>> containertools.split_container_at_index(voice[1], 1, fracture_spanners=False)
        (Measure(1/8, [f'8]), Measure(2/8, [g'8, a'8]))

    ::

        >>> f(voice)
        \new Voice {
            {
                \time 3/8
                c'8 [
                d'8
                e'8
            }
            {
                \time 1/8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8 ]
            }
        }

    Example 2. Split container and fracture crossing spanners::

        >>> voice = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 c'8 c'8") * 2)
        >>> tuplet = voice[1]
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
        >>> beam = beamtools.BeamSpanner(voice[:])

    ::

        >>> f(voice)
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8 ]
            }
        }

    ::

        >>> left, right = containertools.split_container_at_index(
        ...         tuplet, 1, fracture_spanners=True)

    ::

        >>> f(voice)
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                f'8 ]
            }
            \times 2/3 {
                g'8 [
                a'8 ]
            }
        }

    Leave spanners and leaves untouched.

    Resize resizable containers.

    Preserve container multiplier.

    Preserve meter denominator.

    Return split parts.
    '''
    from abjad.tools import spannertools
    from abjad.tools import containertools
    from abjad.tools import contexttools
    from abjad.tools import measuretools
    from abjad.tools import tuplettools

    # convenience leaf index split definition
    if isinstance(component, leaftools.Leaf):
        #raise Exception # debug
        if i <= 0:
            if fracture_spanners:
                spannertools.fracture_spanners_attached_to_component(component, direction=Left)
            return None, component
        else:
            if fracture_spanners:
                spannertools.fracture_spanners_attached_to_component(component, direction=Right)
            return component, None

    # remember container multiplier, if any
    #container_multiplier = getattr(component.duration, 'multiplier', None)
    container_multiplier = getattr(component, 'multiplier', None)

    # partition music of input container
    left_music = component[:i]
    right_music = component[i:]

    # instantiate new left and right containers
    if isinstance(component, measuretools.Measure):
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
    elif isinstance(component, tuplettools.FixedDurationTuplet):
        left = component.__class__(1, left_music)
        right = component.__class__(1, right_music)
        containertools.set_container_multiplier(left, container_multiplier)
        containertools.set_container_multiplier(right, container_multiplier)
    elif isinstance(component, tuplettools.Tuplet):
        left = component.__class__(container_multiplier, left_music)
        right = component.__class__(container_multiplier, right_music)
    else:
        left = component.__class__(left_music)
        right = component.__class__(right_music)
        containertools.set_container_multiplier(left, container_multiplier)
        containertools.set_container_multiplier(right, container_multiplier)

    # save left and right halves together for iteration
    halves = [left, right]
    nonempty_halves = [half for half in halves if len(half)]

    # give attached spanners to children
    spannertools.move_spanners_from_component_to_children_of_component(component)

    # incorporate left and right parents in score, if possible
    parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([component])
    if parent is not None:
        # to avoid pychecker slice assignment error
        #parent._music[start:stop+1] = nonempty_halves
        parent._music.__setitem__(slice(start, stop + 1), nonempty_halves)
        for part in nonempty_halves:
            part._switch(parent)
    else:
        left._switch(None)
        right._switch(None)

    # fracture spanners, if requested
    if fracture_spanners:
        if len(halves) == 2:
            spannertools.fracture_spanners_attached_to_component(left, direction=Right)

    # return new left and right halves
    return left, right
