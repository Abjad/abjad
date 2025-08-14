import bisect

from . import _updatelib
from . import duration as _duration
from . import exceptions as _exceptions
from . import indicators as _indicators
from . import instruments as _instruments
from . import parentage as _parentage
from . import pitch as _pitch
from . import score as _score
from . import timespan as _timespan
from . import wrapper as _wrapper

_dummy = _parentage


def _get_duration_in_seconds(component: _score.Component) -> _duration.Duration:
    if isinstance(component, _score.Container):
        durations = [_get_duration_in_seconds(_) for _ in component]
        if component.simultaneous():
            return max(durations)
        else:
            return sum(durations, start=_duration.Duration(0))
    else:
        mark = get_effective_indicator(component, _indicators.MetronomeMark)
        if mark is not None and mark.is_imprecise() is False:
            fraction = component._get_duration() / mark.reference_duration
            fraction = fraction / mark.units_per_minute * 60
            assert _duration.is_fraction(fraction), repr(fraction)
            return _duration.Duration(fraction)
        raise _exceptions.MissingMetronomeMarkError


def get_duration(
    argument, *, in_seconds: bool = False, preprolated: bool = False
) -> _duration.Duration:
    if preprolated is True:
        if hasattr(argument, "_get_preprolated_duration"):
            duration = argument._get_preprolated_duration()
        else:
            duration = sum(_._get_preprolated_duration() for _ in argument)
        return duration
    if isinstance(argument, _score.Component):
        if in_seconds is True:
            return _get_duration_in_seconds(argument)
        else:
            return argument._get_duration()
    durations = [get_duration(_, in_seconds=in_seconds) for _ in argument]
    return _duration.Duration(sum(durations))


def get_effective_indicator(
    component: _score.Component, prototype, *, attributes=None, command=None, n: int = 0
):
    wrapper = get_effective_wrapper(
        component,
        prototype,
        attributes=attributes,
        command=command,
        n=n,
    )
    if wrapper is not None:
        return wrapper.unbundle_indicator()


def get_effective_wrapper(
    component: _score.Component, prototype, *, attributes=None, command=None, n=0
) -> _wrapper.Wrapper | None:
    _updatelib._update_now(component, indicators=True)
    offset_to_wrapper: dict[_duration.Offset, list[_wrapper.Wrapper]] = {}
    parentage = component._get_parentage()
    enclosing_voice_name = None
    for component_ in parentage:
        if isinstance(component_, _score.Voice):
            if (
                enclosing_voice_name is not None
                and component_.name() != enclosing_voice_name
            ):
                continue
            else:
                enclosing_voice_name = component_.name() or id(component_)
        local_wrappers = []
        for wrapper_ in component_._wrappers:
            if wrapper_.annotation():
                continue
            if isinstance(wrapper_.unbundle_indicator(), prototype):
                append_wrapper = True
                if (
                    command is not None
                    and wrapper_.unbundle_indicator().command != command
                ):
                    continue
                if attributes is not None:
                    for name, value in attributes.items():
                        if getattr(wrapper_.unbundle_indicator(), name, None) != value:
                            append_wrapper = False
                if not append_wrapper:
                    continue
                local_wrappers.append(wrapper_)
        # active indicator takes precendence over inactive indicator
        if any(_.deactivate() is True for _ in local_wrappers) and not all(
            _.deactivate() is True for _ in local_wrappers
        ):
            local_wrappers = [_ for _ in local_wrappers if _.deactivate() is not True]
        for wrapper_ in local_wrappers:
            offset = wrapper_.start_offset()
            offset_to_wrapper.setdefault(offset, []).append(wrapper_)
        if not isinstance(component_, _score.Context):
            continue
        for wrapper_ in component_._dependent_wrappers:
            if wrapper_.annotation():
                continue
            if isinstance(wrapper_.unbundle_indicator(), prototype):
                append_wrapper = True
                if (
                    command is not None
                    and wrapper_.unbundle_indicator().command != command
                ):
                    continue
                if attributes is not None:
                    for name, value in attributes.items():
                        if getattr(wrapper_.unbundle_indicator(), name, None) != value:
                            append_wrapper = False
                if not append_wrapper:
                    continue
                offset = wrapper_.start_offset()
                offset_to_wrapper.setdefault(offset, []).append(wrapper_)
    if not offset_to_wrapper:
        return None
    all_offsets = sorted(offset_to_wrapper)
    start_offset = component._get_timespan().start_offset
    index = bisect.bisect(all_offsets, start_offset) - 1 + int(n)
    if index < 0:
        return None
    elif len(offset_to_wrapper) <= index:
        return None
    wrapper_ = offset_to_wrapper[all_offsets[index]][0]
    return wrapper_


def get_sounding_pitch(note: _score.Note) -> _pitch.NamedPitch:
    note_written_pitch = note.written_pitch()
    assert isinstance(note_written_pitch, _pitch.NamedPitch)
    if "sounding pitch" in note._get_indicators(str):
        return note_written_pitch
    else:
        instrument = get_effective_indicator(note, _instruments.Instrument)
        if instrument:
            sounding_pitch = instrument.middle_c_sounding_pitch
        else:
            sounding_pitch = _pitch.NamedPitch("C4")
        interval = _pitch.NamedPitch("C4") - sounding_pitch
        sounding_pitch = interval.transpose(note_written_pitch)
        return sounding_pitch


def get_sounding_pitches(chord: _score.Chord) -> tuple[_pitch.NamedPitch, ...]:
    chord_written_pitches = chord.written_pitches()
    if "sounding pitch" in chord._get_indicators(str):
        return chord_written_pitches
    else:
        instrument = get_effective_indicator(chord, _instruments.Instrument)
        if instrument:
            sounding_pitch = instrument.middle_c_sounding_pitch
        else:
            sounding_pitch = _pitch.NamedPitch("C4")
        interval = _pitch.NamedPitch("C4") - sounding_pitch
        sounding_pitches = [interval.transpose(_) for _ in chord_written_pitches]
        return tuple(sounding_pitches)


def get_timespan(argument, in_seconds: bool = False) -> _timespan.Timespan:
    if isinstance(argument, _score.Component):
        return argument._get_timespan(in_seconds=in_seconds)
    remaining_items = []
    for i, item in enumerate(argument):
        if i == 0:
            first_item = item
        else:
            remaining_items.append(item)
    timespan = get_timespan(first_item, in_seconds=in_seconds)
    start_offset = timespan.start_offset
    stop_offset = timespan.stop_offset
    for item in remaining_items:
        timespan = get_timespan(item, in_seconds=in_seconds)
        if timespan.start_offset < start_offset:
            start_offset = timespan.start_offset
        if stop_offset < timespan.stop_offset:
            stop_offset = timespan.stop_offset
    return _timespan.Timespan(start_offset, stop_offset)


def is_grace_container(component: _score.Component) -> bool:
    # _score.IndependentAfterGraceContainer is excluded here;
    # exclusion allows iteration to work correctly
    prototype = (
        _score.AfterGraceContainer,
        _score.BeforeGraceContainer,
    )
    for component_ in component._get_parentage():
        if isinstance(component_, prototype):
            return True
        if component_.__class__.__name__ == "OnBeatGraceContainer":
            return True
    return False
