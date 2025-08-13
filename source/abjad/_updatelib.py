"""
Updates start offsets, stop offsets and indicators everywhere in score.

..  note:: This is probably the most important part of Abjad to optimize. Use
    the profiler to figure out how many unnecessary updates are happening. Then
    reimplement. As a hint, _updatelib.py implements a weird version of the
    "observer pattern." It may make sense to revisit a textbook example of the
    observer pattern and review the implementation here.

"""

import dataclasses
import fractions

from . import duration as _duration
from . import indicators as _indicators
from . import iterate as _iterate
from . import obgc as _obgc
from . import parentage as _parentage
from . import score as _score
from . import sequence as _sequence
from . import timespan as _timespan


def _get_after_grace_leaf_offsets(
    leaf,
) -> tuple[_duration.Offset, _duration.Offset]:
    container = leaf._parent
    main_leaf = container._main_leaf
    main_leaf_stop_offset = main_leaf._timespan.value_stop_offset()
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
    if displacement == 0:
        start_offset = main_leaf_stop_offset
    else:
        start_offset = dataclasses.replace(
            main_leaf_stop_offset,
            displacement=displacement,
        )
    displacement += leaf._get_duration()
    if displacement == 0:
        stop_offset = main_leaf_stop_offset
    else:
        stop_offset = dataclasses.replace(
            main_leaf_stop_offset,
            displacement=displacement,
        )
    return start_offset, stop_offset


def _get_before_grace_leaf_offsets(
    leaf,
) -> tuple[_duration.Offset, _duration.Offset]:
    container = leaf._parent
    main_leaf = container._main_leaf
    main_leaf_start_offset = main_leaf._timespan.value_start_offset()
    assert main_leaf_start_offset is not None
    displacement = -leaf._get_duration()
    sibling = leaf._sibling(1)
    while sibling is not None and sibling._parent is container:
        displacement -= sibling._get_duration()
        sibling = sibling._sibling(1)
    if displacement == 0:
        start_offset = dataclasses.replace(main_leaf_start_offset)
    else:
        start_offset = dataclasses.replace(
            main_leaf_start_offset,
            displacement=displacement,
        )
    displacement += leaf._get_duration()
    if displacement == 0:
        stop_offset = dataclasses.replace(main_leaf_start_offset)
    else:
        stop_offset = dataclasses.replace(
            main_leaf_start_offset,
            displacement=displacement,
        )
    return start_offset, stop_offset


def _get_independent_after_grace_leaf_offsets(
    leaf,
) -> tuple[_duration.Offset, _duration.Offset]:
    container = leaf._parent
    main_leaf = container._sibling(-1)
    main_leaf_stop_offset = main_leaf._timespan.value_stop_offset()
    assert main_leaf_stop_offset is not None
    displacement = -leaf._get_duration()
    sibling = leaf._sibling(1)
    while sibling is not None and sibling._parent is container:
        displacement -= sibling._get_duration()
        sibling = sibling._sibling(1)
    """
    if leaf._parent is not None and leaf._parent._sibling(-1) is not None:
        main_leaf = leaf._parent._sibling(-1)
        sibling = main_leaf._sibling(1)
        if (
            sibling is not None
            and hasattr(sibling, "_before_grace_container")
            and sibling._before_grace_container is not None
        ):
            before_grace_container = sibling._before_grace_container
            duration = before_grace_container._get_duration()
            displacement -= duration
    """
    if displacement == 0:
        start_offset = dataclasses.replace(main_leaf_stop_offset)
    else:
        start_offset = dataclasses.replace(
            main_leaf_stop_offset,
            displacement=displacement,
        )
    displacement += leaf._get_duration()
    if displacement == 0:
        stop_offset = dataclasses.replace(main_leaf_stop_offset)
    else:
        stop_offset = dataclasses.replace(
            main_leaf_stop_offset,
            displacement=displacement,
        )
    return start_offset, stop_offset


def _get_measure_start_offsets(component) -> list[_duration.Offset]:
    wrappers = []
    prototype = _indicators.TimeSignature
    root = _parentage.Parentage(component).root()
    for component_ in _iterate_entire_score(root):
        wrappers_ = component_._get_wrappers(prototype)
        wrappers.extend(wrappers_)
    pairs = []
    for wrapper in wrappers:
        component = wrapper.component()
        start_offset = component._get_timespan().value_start_offset()
        time_signature = wrapper.unbundle_indicator()
        pair = start_offset, time_signature
        pairs.append(pair)
    offset_zero = _duration.mvo(0)
    default_time_signature = _indicators.TimeSignature((4, 4))
    default_pair = (offset_zero, default_time_signature)
    if pairs and not pairs[0] == offset_zero:
        pairs.insert(0, default_pair)
    elif not pairs:
        pairs = [default_pair]
    pairs.sort(key=lambda x: x[0])
    score_stop_offset = root._get_timespan().value_stop_offset()
    dummy_last_pair = (score_stop_offset, None)
    pairs.append(dummy_last_pair)
    measure_start_offsets = []
    at_first_measure = True
    for current_pair, next_pair in _sequence.nwise(pairs):
        current_start_offset, current_time_signature = current_pair
        next_start_offset, next_time_signature = next_pair
        measure_start_offset = current_start_offset
        assert isinstance(measure_start_offset, _duration.Offset)
        assert isinstance(current_start_offset, _duration.Offset)
        while measure_start_offset < next_start_offset:
            measure_start_offsets.append(measure_start_offset)
            partial = current_time_signature.partial
            if at_first_measure and partial is not None:
                measure_start_offset += partial
                measure_start_offsets.append(measure_start_offset)
                at_first_measure = False
            measure_start_offset += current_time_signature.duration()
    assert all(isinstance(_, _duration.Offset) for _ in measure_start_offsets)
    return measure_start_offsets


def _get_obgc_leaf_offsets(leaf) -> tuple[_duration.Offset, _duration.Offset]:
    obgc = leaf._parent
    assert type(obgc).__name__ == "OnBeatGraceContainer", repr(obgc)
    first_nongrace_leaf = obgc.first_nongrace_leaf()
    first_nongrace_leaf_start_offset = (
        first_nongrace_leaf._timespan.value_start_offset()
    )
    assert first_nongrace_leaf_start_offset is not None
    first_nongrace_leaf_start_offset = dataclasses.replace(
        first_nongrace_leaf_start_offset
    )
    start_displacement: _duration.Duration | None = _duration.Duration(0)
    sibling = leaf._sibling(-1)
    while sibling is not None and sibling._parent is obgc:
        start_displacement += sibling._get_duration()
        sibling = sibling._sibling(-1)
    stop_displacement = start_displacement + leaf._get_duration()
    if start_displacement == 0:
        start_displacement = None
    start_offset = dataclasses.replace(
        first_nongrace_leaf_start_offset,
        displacement=start_displacement,
    )
    stop_offset = dataclasses.replace(
        first_nongrace_leaf_start_offset,
        displacement=stop_displacement,
    )
    return start_offset, stop_offset


def _get_score_tree_state_flags(parentage) -> tuple[bool, bool, bool]:
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
    components = list(_iterate.components(root, grace=False))
    graces = _iterate.components(root, grace=True)
    components.extend(graces)
    return components


def _make_metronome_mark_map(root) -> _timespan.TimespanList | None:
    pairs = []
    all_stop_offsets = set()
    for component in _iterate_entire_score(root):
        indicators = component._get_indicators(_indicators.MetronomeMark)
        if len(indicators) == 1:
            metronome_mark = indicators[0]
            if not metronome_mark.is_imprecise():
                pair = (
                    component._timespan.value_start_offset(),
                    metronome_mark,
                )
                pairs.append(pair)
        all_stop_offsets.add(component._timespan.value_stop_offset())
    pairs.sort(key=lambda _: _[0])
    if not pairs:
        return None
    if pairs[0][0] != _duration.mvo(0):
        return None
    score_stop_offset = max(all_stop_offsets)
    timespans = _timespan.TimespanList()
    clocktime_start_offset = _duration.mvo(0)
    for left, right in _sequence.nwise(pairs, wrapped=True):
        metronome_mark = left[-1]
        start_offset = left[0]
        stop_offset = right[0]
        # last timespan
        if stop_offset == _duration.mvo(0):
            stop_offset = score_stop_offset
        duration = stop_offset - start_offset
        multiplier = fractions.Fraction(60, metronome_mark.units_per_minute)
        clocktime_duration = duration / metronome_mark.reference_duration
        clocktime_duration *= multiplier
        timespan = _timespan.Timespan(
            start_offset,
            stop_offset,
            annotation=(clocktime_start_offset, clocktime_duration),
        )
        timespans.append(timespan)
        clocktime_start_offset += clocktime_duration
    return timespans


def _to_measure_number(
    component,
    measure_start_offsets: list[_duration.Offset],
) -> int:
    assert all(isinstance(_, _duration.Offset) for _ in measure_start_offsets)
    component_start_offset = component._get_timespan().value_start_offset()
    displacement = component_start_offset.displacement
    if displacement is not None:
        assert isinstance(displacement, _duration.Duration), repr(displacement)
        # score-initial grace music only:
        if displacement < 0 and component_start_offset.fraction == 0:
            measure_number = 0
            return measure_number
    measure_start_offsets = measure_start_offsets[:]
    # measure_start_offsets.append(_math.Infinity())
    # TODO: model with infinity:
    measure_start_offsets.append(_duration.Offset(fractions.Fraction(1000000000)))
    pairs = _sequence.nwise(measure_start_offsets)
    for measure_index, pair in enumerate(pairs):
        assert all(isinstance(_, _duration.Offset) for _ in pair)
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
        for wrapper in component._get_wrappers():
            if wrapper.context_name() is not None:
                wrapper._update_effective_context()
        component._indicators_are_current = True


def _update_all_offsets(root):
    """
    Updating offsets does not update indicators.
    Updating offsets does not update offsets in seconds.
    """
    obgc_components = []
    for component in _iterate_entire_score(root):
        if isinstance(component, _obgc.OnBeatGraceContainer) or isinstance(
            component._parent, _obgc.OnBeatGraceContainer
        ):
            obgc_components.append(component)
        else:
            _update_component_offsets(component)
            component._offsets_are_current = True
    for component in obgc_components:
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
        if (
            timespan.value_start_offset()
            <= component._timespan.value_start_offset()
            < timespan.value_stop_offset()
        ):
            pair = timespan.annotation
            clocktime_start_offset, clocktime_duration = pair
            local_offset = (
                component._timespan.value_start_offset() - timespan.value_start_offset()
            )
            multiplier = local_offset / timespan.duration()
            duration = multiplier * clocktime_duration
            offset = clocktime_start_offset + duration
            assert isinstance(offset, _duration.Offset)
            component._start_offset_in_seconds = offset
        if (
            timespan.value_start_offset()
            <= component._timespan.value_stop_offset()
            < timespan.value_stop_offset()
        ):
            pair = timespan.annotation
            clocktime_start_offset, clocktime_duration = pair
            local_offset = (
                component._timespan.value_stop_offset() - timespan.value_start_offset()
            )
            multiplier = local_offset / timespan.duration()
            duration = multiplier * clocktime_duration
            offset = clocktime_start_offset + duration
            assert isinstance(offset, _duration.Offset)
            component._stop_offset_in_seconds = offset
            return
    if component._timespan.value_stop_offset() == timespans[-1].value_stop_offset():
        pair = timespans[-1].annotation
        clocktime_start_offset, clocktime_duration = pair
        offset = clocktime_start_offset + clocktime_duration
        assert isinstance(offset, _duration.Offset)
        component._stop_offset_in_seconds = offset
        return
    raise Exception(f"can not find {offset!r} in {timespans}.")


def _update_component_offsets(component) -> None:
    if isinstance(component, _score.BeforeGraceContainer):
        pair = _get_before_grace_leaf_offsets(component[0])
        start_offset = pair[0]
        pair = _get_before_grace_leaf_offsets(component[-1])
        stop_offset = pair[-1]
    elif isinstance(component._parent, _score.BeforeGraceContainer):
        pair = _get_before_grace_leaf_offsets(component)
        start_offset = pair[0]
        stop_offset = pair[-1]
    elif isinstance(component, _obgc.OnBeatGraceContainer):
        pair = _get_obgc_leaf_offsets(component[0])
        start_offset = pair[0]
        pair = _get_obgc_leaf_offsets(component[-1])
        stop_offset = pair[-1]
    elif isinstance(component._parent, _obgc.OnBeatGraceContainer):
        pair = _get_obgc_leaf_offsets(component)
        start_offset = pair[0]
        stop_offset = pair[1]
    elif isinstance(component, _score.AfterGraceContainer):
        pair = _get_after_grace_leaf_offsets(component[0])
        start_offset = pair[0]
        pair = _get_after_grace_leaf_offsets(component[-1])
        stop_offset = pair[-1]
    elif isinstance(component, _score.IndependentAfterGraceContainer):
        pair = _get_independent_after_grace_leaf_offsets(component[0])
        start_offset = pair[0]
        pair = _get_independent_after_grace_leaf_offsets(component[-1])
        stop_offset = pair[-1]
    elif isinstance(component._parent, _score.AfterGraceContainer):
        pair = _get_after_grace_leaf_offsets(component)
        start_offset = pair[0]
        stop_offset = pair[1]
    elif isinstance(component._parent, _score.IndependentAfterGraceContainer):
        pair = _get_independent_after_grace_leaf_offsets(component)
        start_offset = pair[0]
        stop_offset = pair[1]
    else:
        previous = component._sibling(-1)
        if previous is not None:
            start_offset = previous._timespan.value_stop_offset()
        else:
            start_offset = _duration.mvo(0)
        # on-beat anchor leaf:
        if (
            component._parent is not None
            and _obgc._is_obgc_nongrace_voice(component._parent)
            and component is component._parent[0]
        ):
            assert isinstance(start_offset, _duration.Offset)
            nongrace_voice = component._parent
            assert _obgc._is_obgc_nongrace_voice(nongrace_voice)
            obgc = None
            polyphony_container = nongrace_voice._parent
            assert _obgc._is_obgc_polyphony_container(polyphony_container)
            index = polyphony_container.index(nongrace_voice)
            # TODO: limit OBGC to index 0 (not index 1) in polyphony container
            if index == 0:
                obgc = polyphony_container[1]
            else:
                obgc = polyphony_container[0]
            if obgc is not None:
                grace_leaf_durations = [_._get_duration() for _ in obgc]
                start_displacement = sum(grace_leaf_durations)
                start_offset = dataclasses.replace(
                    start_offset,
                    displacement=start_displacement,
                )
        assert isinstance(start_offset, _duration.Offset), repr(start_offset)
        stop_offset_duration = start_offset.fraction + component._get_duration()
        stop_offset = _duration.Offset(stop_offset_duration.fraction())
    assert isinstance(start_offset, _duration.Offset), repr(start_offset)
    assert isinstance(stop_offset, _duration.Offset), repr(stop_offset)
    timespan = _timespan.Timespan(start_offset, stop_offset)
    component._timespan = timespan


def _update_measure_numbers(main_component) -> None:
    measure_start_offsets = _get_measure_start_offsets(main_component)
    root = _parentage.Parentage(main_component).root()
    for component in _iterate_entire_score(root):
        measure_number = _to_measure_number(component, measure_start_offsets)
        component._measure_number = measure_number


def _update_now(component, offsets=False, offsets_in_seconds=False, indicators=False):
    assert offsets or offsets_in_seconds or indicators
    parentage = component._get_parentage()
    for component_ in parentage:
        if component_._is_forbidden_to_update:
            return
    (
        offsets_are_current,
        indicators_are_current,
        offsets_in_seconds_are_current,
    ) = _get_score_tree_state_flags(parentage)
    root = parentage[-1]
    if offsets and not offsets_are_current:
        _update_all_offsets(root)
    if offsets_in_seconds and not offsets_in_seconds_are_current:
        _update_all_offsets_in_seconds(root)
    if indicators and not indicators_are_current:
        _update_all_indicators(root)
