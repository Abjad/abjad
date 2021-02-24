"""
Updates start offsets, stop offsets and indicators everywhere in score.

..  note:: This is probably the most important part of Abjad to optimize.
    Use the profiler to figure out how many unnecessary updates are
    happening. Then reimplement. As a hint, the update manager implements
    a weird version of the "observer pattern." It may make sense to revisit
    a textbook example of the observer pattern and review the
    implementation of the update manager.

"""
from . import math
from .duration import Duration, Multiplier, Offset
from .indicators.MetronomeMark import MetronomeMark
from .indicators.TimeSignature import TimeSignature
from .iterate import Iteration
from .obgc import OnBeatGraceContainer
from .parentage import Parentage
from .score import AfterGraceContainer, BeforeGraceContainer
from .sequence import Sequence
from .timespan import AnnotatedTimespan, TimespanList


def _get_after_grace_leaf_offsets(leaf):
    container = leaf._parent
    main_leaf = container._main_leaf
    main_leaf_stop_offset = main_leaf._stop_offset
    assert main_leaf_stop_offset is not None
    displacement = -leaf._get_duration()
    sibling = leaf._sibling(1)
    while sibling is not None and sibling._parent is container:
        displacement -= sibling._get_duration()
        sibling = sibling._sibling(1)
    if leaf._parent is not None and leaf._parent._main_leaf is not None:
        main_leaf = leaf._parent._main_leaf
        sibling = main_leaf._sibling(1)
        if (
            sibling is not None
            and hasattr(sibling, "_before_grace_container")
            and sibling._before_grace_container is not None
        ):
            before_grace_container = sibling._before_grace_container
            duration = before_grace_container._get_duration()
            displacement -= duration
    start_offset = Offset(main_leaf_stop_offset, displacement=displacement)
    displacement += leaf._get_duration()
    stop_offset = Offset(main_leaf_stop_offset, displacement=displacement)
    return start_offset, stop_offset


def _get_before_grace_leaf_offsets(leaf):
    container = leaf._parent
    main_leaf = container._main_leaf
    main_leaf_start_offset = main_leaf._start_offset
    assert main_leaf_start_offset is not None
    displacement = -leaf._get_duration()
    sibling = leaf._sibling(1)
    while sibling is not None and sibling._parent is container:
        displacement -= sibling._get_duration()
        sibling = sibling._sibling(1)
    start_offset = Offset(main_leaf_start_offset, displacement=displacement)
    displacement += leaf._get_duration()
    stop_offset = Offset(main_leaf_start_offset, displacement=displacement)
    return start_offset, stop_offset


def _get_measure_start_offsets(component):
    wrappers = []
    prototype = TimeSignature
    root = Parentage(component).root
    for component_ in _iterate_entire_score(root):
        wrappers_ = component_._get_indicators(prototype, unwrap=False)
        wrappers.extend(wrappers_)
    pairs = []
    for wrapper in wrappers:
        component = wrapper.component
        start_offset = component._get_timespan().start_offset
        time_signature = wrapper.indicator
        pair = start_offset, time_signature
        pairs.append(pair)
    offset_zero = Offset(0)
    default_time_signature = TimeSignature((4, 4))
    default_pair = (offset_zero, default_time_signature)
    if pairs and not pairs[0] == offset_zero:
        pairs.insert(0, default_pair)
    elif not pairs:
        pairs = [default_pair]
    pairs.sort(key=lambda x: x[0])
    score_stop_offset = root._get_timespan().stop_offset
    dummy_last_pair = (score_stop_offset, None)
    pairs.append(dummy_last_pair)
    measure_start_offsets = []
    at_first_measure = True
    for current_pair, next_pair in Sequence(pairs).nwise():
        current_start_offset, current_time_signature = current_pair
        next_start_offset, next_time_signature = next_pair
        measure_start_offset = current_start_offset
        while measure_start_offset < next_start_offset:
            measure_start_offsets.append(measure_start_offset)
            partial = current_time_signature.partial
            if at_first_measure and partial is not None:
                measure_start_offset += partial
                measure_start_offsets.append(measure_start_offset)
                at_first_measure = False
            measure_start_offset += current_time_signature.duration
    return measure_start_offsets


def _get_on_beat_grace_leaf_offsets(leaf):
    container = leaf._parent
    anchor_leaf = container._get_on_beat_anchor_leaf()
    anchor_leaf_start_offset = anchor_leaf._start_offset
    assert anchor_leaf_start_offset is not None
    anchor_leaf_start_offset = Offset(anchor_leaf_start_offset.pair)
    start_displacement = Duration(0)
    sibling = leaf._sibling(-1)
    while sibling is not None and sibling._parent is container:
        start_displacement += sibling._get_duration()
        sibling = sibling._sibling(-1)
    stop_displacement = start_displacement + leaf._get_duration()
    if start_displacement == 0:
        start_displacement = None
    start_offset = Offset(
        anchor_leaf_start_offset.pair, displacement=start_displacement
    )
    stop_offset = Offset(anchor_leaf_start_offset.pair, displacement=stop_displacement)
    return start_offset, stop_offset


def _get_score_tree_state_flags(parentage):
    offsets_are_current = True
    indicators_are_current = True
    offsets_in_seconds_are_current = True
    for component in parentage:
        if offsets_are_current:
            if not component._offsets_are_current:
                offsets_are_current = False
        if indicators_are_current:
            if not component._indicators_are_current:
                indicators_are_current = False
        if offsets_in_seconds_are_current:
            if not component._offsets_in_seconds_are_current:
                offsets_in_seconds_are_current = False
    return (
        offsets_are_current,
        indicators_are_current,
        offsets_in_seconds_are_current,
    )


def _iterate_entire_score(root):
    """
    NOTE: RETURNS GRACE NOTES LAST (AND OUT-OF-ORDER).
    """
    components = list(Iteration(root).components(grace=False))
    graces = Iteration(root).components(grace=True)
    components.extend(graces)
    return components


def _make_metronome_mark_map(root):
    pairs = []
    all_stop_offsets = set()
    for component in _iterate_entire_score(root):
        indicators = component._get_indicators(MetronomeMark)
        if len(indicators) == 1:
            metronome_mark = indicators[0]
            if not metronome_mark.is_imprecise:
                pair = (component._start_offset, metronome_mark)
                pairs.append(pair)
        if component._stop_offset is not None:
            all_stop_offsets.add(component._stop_offset)
    pairs.sort(key=lambda _: _[0])
    if not pairs:
        return
    if pairs[0][0] != 0:
        return
    score_stop_offset = max(all_stop_offsets)
    timespans = TimespanList()
    clocktime_start_offset = Offset(0)
    for left, right in Sequence(pairs).nwise(wrapped=True):
        metronome_mark = left[-1]
        start_offset = left[0]
        stop_offset = right[0]
        # last timespan
        if stop_offset == 0:
            stop_offset = score_stop_offset
        duration = stop_offset - start_offset
        multiplier = Multiplier(60, metronome_mark.units_per_minute)
        clocktime_duration = duration / metronome_mark.reference_duration
        clocktime_duration *= multiplier
        timespan = AnnotatedTimespan(
            start_offset=start_offset,
            stop_offset=stop_offset,
            annotation=(clocktime_start_offset, clocktime_duration),
        )
        timespans.append(timespan)
        clocktime_start_offset += clocktime_duration
    return timespans


# TODO: reimplement with some type of bisection
def _to_measure_number(component, measure_start_offsets):
    component_start_offset = component._get_timespan().start_offset
    displacement = component_start_offset.displacement
    if displacement is not None:
        component_start_offset = Offset(component_start_offset, displacement=None)
        # score-initial grace music only:
        if displacement < 0 and component_start_offset == 0:
            measure_number = 0
            return measure_number
    measure_start_offsets = measure_start_offsets[:]
    measure_start_offsets.append(math.Infinity())
    pairs = Sequence(measure_start_offsets)
    pairs = pairs.nwise()
    for measure_index, pair in enumerate(pairs):
        if pair[0] <= component_start_offset < pair[-1]:
            measure_number = measure_index + 1
            return measure_number
    message = f"can not find measure number for {repr(component)}:\n"
    message += f"   {repr(measure_start_offsets)}"
    raise ValueError(message)


def _update_all_indicators(root):
    """
    Updating indicators does not update offsets.
    On the other hand, getting an effective indicator does update
    offsets when at least one indicator of the appropriate type
    attaches to score.
    """
    components = _iterate_entire_score(root)
    for component in components:
        for wrapper in component._get_indicators(unwrap=False):
            if wrapper.context is not None:
                wrapper._update_effective_context()
        component._indicators_are_current = True


def _update_all_offsets(root):
    """
    Updating offsets does not update indicators.
    Updating offsets does not update offsets in seconds.
    """
    on_beat_grace_music = []
    for component in _iterate_entire_score(root):
        if isinstance(component, OnBeatGraceContainer) or isinstance(
            component._parent, OnBeatGraceContainer
        ):
            on_beat_grace_music.append(component)
        else:
            _update_component_offsets(component)
            component._offsets_are_current = True
    for component in on_beat_grace_music:
        _update_component_offsets(component)
        component._offsets_are_current = True


def _update_all_offsets_in_seconds(root):
    _update_all_offsets(root)
    timespans = _make_metronome_mark_map(root)
    for component in _iterate_entire_score(root):
        _update_clocktime_offsets(component, timespans)
        component._offsets_in_seconds_are_current = True


def _update_clocktime_offsets(component, timespans):
    if not timespans:
        return
    for timespan in timespans:
        if timespan.start_offset <= component._start_offset < timespan.stop_offset:
            pair = timespan.annotation
            clocktime_start_offset, clocktime_duration = pair
            local_offset = component._start_offset - timespan.start_offset
            multiplier = local_offset / timespan.duration
            duration = multiplier * clocktime_duration
            offset = clocktime_start_offset + duration
            component._start_offset_in_seconds = Offset(offset)
        if timespan.start_offset <= component._stop_offset < timespan.stop_offset:
            pair = timespan.annotation
            clocktime_start_offset, clocktime_duration = pair
            local_offset = component._stop_offset - timespan.start_offset
            multiplier = local_offset / timespan.duration
            duration = multiplier * clocktime_duration
            offset = clocktime_start_offset + duration
            component._stop_offset_in_seconds = Offset(offset)
            return
    if component._stop_offset == timespans[-1].stop_offset:
        pair = timespans[-1].annotation
        clocktime_start_offset, clocktime_duration = pair
        offset = clocktime_start_offset + clocktime_duration
        component._stop_offset_in_seconds = Offset(offset)
        return
    raise Exception(f"can not find {offset} in {timespans}.")


def _update_component_offsets(component):
    if isinstance(component, BeforeGraceContainer):
        pair = _get_before_grace_leaf_offsets(component[0])
        start_offset = pair[0]
        pair = _get_before_grace_leaf_offsets(component[-1])
        stop_offset = pair[-1]
    elif isinstance(component._parent, BeforeGraceContainer):
        pair = _get_before_grace_leaf_offsets(component)
        start_offset, stop_offset = pair
    elif isinstance(component, OnBeatGraceContainer):
        pair = _get_on_beat_grace_leaf_offsets(component[0])
        start_offset = pair[0]
        pair = _get_on_beat_grace_leaf_offsets(component[-1])
        stop_offset = pair[-1]
    elif isinstance(component._parent, OnBeatGraceContainer):
        pair = _get_on_beat_grace_leaf_offsets(component)
        start_offset, stop_offset = pair
    elif isinstance(component, AfterGraceContainer):
        pair = _get_after_grace_leaf_offsets(component[0])
        start_offset = pair[0]
        pair = _get_after_grace_leaf_offsets(component[-1])
        stop_offset = pair[-1]
    elif isinstance(component._parent, AfterGraceContainer):
        pair = _get_after_grace_leaf_offsets(component)
        start_offset, stop_offset = pair
    else:
        previous = component._sibling(-1)
        if previous is not None:
            start_offset = previous._stop_offset
        else:
            start_offset = Offset(0)
        # on-beat anchor leaf:
        if (
            component._parent is not None
            and OnBeatGraceContainer._is_on_beat_anchor_voice(component._parent)
            and component is component._parent[0]
        ):
            anchor_voice = component._parent
            assert OnBeatGraceContainer._is_on_beat_anchor_voice(anchor_voice)
            on_beat_grace_container = None
            on_beat_wrapper = anchor_voice._parent
            assert OnBeatGraceContainer._is_on_beat_wrapper(on_beat_wrapper)
            index = on_beat_wrapper.index(anchor_voice)
            if index == 0:
                on_beat_grace_container = on_beat_wrapper[1]
            else:
                on_beat_grace_container = on_beat_wrapper[0]
            if on_beat_grace_container is not None:
                durations = [_._get_duration() for _ in on_beat_grace_container]
                start_displacement = sum(durations)
                start_offset = Offset(start_offset, displacement=start_displacement)
        stop_offset = start_offset + component._get_duration()
    component._start_offset = start_offset
    component._stop_offset = stop_offset
    component._timespan._start_offset = start_offset
    component._timespan._stop_offset = stop_offset


def _update_measure_numbers(component):
    measure_start_offsets = _get_measure_start_offsets(component)
    root = Parentage(component).root
    for component in _iterate_entire_score(root):
        measure_number = _to_measure_number(component, measure_start_offsets)
        component._measure_number = measure_number


def _update_now(component, offsets=False, offsets_in_seconds=False, indicators=False):
    assert offsets or offsets_in_seconds or indicators
    if component._is_forbidden_to_update:
        return
    parentage = Parentage(component)
    for parent in parentage:
        if parent._is_forbidden_to_update:
            return
        (
            offsets_are_current,
            indicators_are_current,
            offsets_in_seconds_are_current,
        ) = _get_score_tree_state_flags(parentage)
    root = parentage.root
    if offsets and not offsets_are_current:
        _update_all_offsets(root)
    if offsets_in_seconds and not offsets_in_seconds_are_current:
        _update_all_offsets_in_seconds(root)
    if indicators and not indicators_are_current:
        _update_all_indicators(root)
