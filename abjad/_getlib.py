import bisect
import collections
import enum
import typing

from . import _updatelib
from . import duration as _duration
from . import exceptions as _exceptions
from . import indicators as _indicators
from . import instruments as _instruments
from . import parentage as _parentage
from . import pitch as _pitch
from . import score as _score
from . import timespan as _timespan
from . import typings as _typings


def _are_logical_voice(components, prototype=None):
    prototype = prototype or (_score.Component,)
    if not isinstance(prototype, tuple):
        prototype = (prototype,)
    assert isinstance(prototype, tuple)
    if len(components) == 0:
        return True
    if all(isinstance(_, prototype) and _._parent is None for _ in components):
        return True
    first = components[0]
    if not isinstance(first, prototype):
        return False
    same_logical_voice = True
    parentage = _parentage.Parentage(first)
    first_logical_voice = parentage.logical_voice()
    for component in components[1:]:
        parentage = _parentage.Parentage(component)
        if parentage.logical_voice() != first_logical_voice:
            same_logical_voice = False
        if not parentage.orphan and not same_logical_voice:
            return False
    return True


def _get_annotation(component, annotation, default=None, unwrap: bool = True):
    assert isinstance(annotation, str | enum.Enum), repr(annotation)
    for wrapper in _get_annotation_wrappers(component):
        if wrapper.annotation == annotation:
            if unwrap is True:
                return wrapper.get_item()
            else:
                return wrapper
    return default


def _get_annotation_wrappers(argument):
    result = []
    for wrapper in getattr(argument, "_wrappers", []):
        if wrapper.annotation:
            result.append(wrapper)
    return result


def _get_duration(argument, *, in_seconds: bool = False, preprolated: bool = False):
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
    durations = [_get_duration(_, in_seconds=in_seconds) for _ in argument]
    return _duration.Duration(sum(durations))


def _get_duration_in_seconds(component):
    if isinstance(component, _score.Container):
        if component.simultaneous:
            return max(
                [_duration.Duration(0)]
                + [_get_duration_in_seconds(_) for _ in component]
            )
        else:
            duration = _duration.Duration(0)
            for component_ in component:
                duration += _get_duration_in_seconds(component_)
            return duration
    else:
        mark = _get_effective(component, _indicators.MetronomeMark)
        if mark is not None and not mark.is_imprecise:
            result = (
                component._get_duration()
                / mark.reference_duration
                / mark.units_per_minute
                * 60
            )
            return _duration.Duration(result)
        raise _exceptions.MissingMetronomeMarkError


def _get_effective(
    component, prototype, *, attributes=None, command=None, n=0, unwrap=True
):
    _updatelib._update_now(component, indicators=True)
    candidate_wrappers = {}
    parentage = component._get_parentage()
    enclosing_voice_name = None
    for component_ in parentage:
        if isinstance(component_, _score.Voice):
            if (
                enclosing_voice_name is not None
                and component_.name != enclosing_voice_name
            ):
                continue
            else:
                enclosing_voice_name = component_.name or id(component_)
        local_wrappers = []
        for wrapper in component_._wrappers:
            if wrapper.annotation:
                continue
            if isinstance(wrapper.unbundle_indicator(), prototype):
                append_wrapper = True
                if (
                    command is not None
                    and wrapper.unbundle_indicator().command != command
                ):
                    continue
                if attributes is not None:
                    for name, value in attributes.items():
                        if getattr(wrapper.unbundle_indicator(), name, None) != value:
                            append_wrapper = False
                if not append_wrapper:
                    continue
                local_wrappers.append(wrapper)
        # active indicator takes precendence over inactive indicator
        if any(_.deactivate is True for _ in local_wrappers) and not all(
            _.deactivate is True for _ in local_wrappers
        ):
            local_wrappers = [_ for _ in local_wrappers if _.deactivate is not True]
        for wrapper in local_wrappers:
            offset = wrapper.start_offset
            candidate_wrappers.setdefault(offset, []).append(wrapper)
        if not isinstance(component_, _score.Context):
            continue
        for wrapper in component_._dependent_wrappers:
            if wrapper.annotation:
                continue
            if isinstance(wrapper.unbundle_indicator(), prototype):
                append_wrapper = True
                if (
                    command is not None
                    and wrapper.unbundle_indicator().command != command
                ):
                    continue
                if attributes is not None:
                    for name, value in attributes.items():
                        if getattr(wrapper.unbundle_indicator(), name, None) != value:
                            append_wrapper = False
                if not append_wrapper:
                    continue
                offset = wrapper.start_offset
                candidate_wrappers.setdefault(offset, []).append(wrapper)
    if not candidate_wrappers:
        return
    all_offsets = sorted(candidate_wrappers)
    start_offset = component._get_timespan().start_offset
    index = bisect.bisect(all_offsets, start_offset) - 1 + int(n)
    if index < 0:
        return
    elif len(candidate_wrappers) <= index:
        return
    wrapper = candidate_wrappers[all_offsets[index]][0]
    if unwrap:
        return wrapper.unbundle_indicator()
    return wrapper


def _get_grace_container(component):
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


def _get_indicator(
    component: _score.Component,
    prototype: _typings.Prototype | None = None,
    *,
    default: typing.Any | None = None,
    unwrap: bool = True,
) -> typing.Any:
    if not isinstance(component, _score.Component):
        raise Exception("can only get indicator on component.")
    indicators = component._get_indicators(prototype=prototype, unwrap=unwrap)
    if not indicators:
        return default
    elif len(indicators) == 1:
        return list(indicators)[0]
    else:
        name = getattr(prototype, "__name__", "")
        strings = "\n".join(["    " + str(_) for _ in indicators])
        string = f"{len(indicators)} {name} indicators attached to {component}:"
        string += f"\n{strings}"
        raise Exception(string)


def _get_leaf_from_leaf(leaf, n):
    assert n in (-1, 0, 1), repr(n)
    if n == 0:
        return leaf
    sibling = leaf._sibling(n)
    if sibling is None:
        return None
    if n == 1:
        components = sibling._get_descendants_starting_with()
    else:
        assert n == -1
        if (
            isinstance(sibling, _score.Container)
            and len(sibling) == 2
            and any(hasattr(_, "_grace_leaf_duration") for _ in sibling)
        ):
            if sibling[0].__class__.__name__ == "OnBeatGraceContainer":
                main_voice = sibling[1]
            else:
                main_voice = sibling[0]
            return main_voice[-1]
        components = sibling._get_descendants_stopping_with()
    for component in components:
        if not isinstance(component, _score.Leaf):
            continue
        if _are_logical_voice([leaf, component]):
            return component


def _get_persistent_wrappers(*, dependent_wrappers=None, omit_with_indicator=None):
    wrappers = {}
    for wrapper in dependent_wrappers:
        if wrapper.annotation:
            continue
        if not getattr(wrapper.unbundle_indicator(), "persistent", False):
            continue
        assert isinstance(wrapper.unbundle_indicator().persistent, bool)
        should_omit = False
        if omit_with_indicator is not None:
            for component in wrapper.component._get_parentage():
                if component._has_indicator(omit_with_indicator):
                    should_omit = True
                    continue
        if should_omit:
            continue
        if hasattr(wrapper.unbundle_indicator(), "parameter"):
            key = wrapper.unbundle_indicator().parameter
        elif isinstance(wrapper.unbundle_indicator(), _instruments.Instrument):
            key = "Instrument"
        else:
            key = str(type(wrapper.unbundle_indicator()))
        if key not in wrappers:
            wrappers[key] = wrapper
        elif (
            wrappers[key].site_adjusted_start_offset
            < wrapper.site_adjusted_start_offset
        ):
            wrappers[key] = wrapper
        elif (
            wrappers[key].site_adjusted_start_offset
            == wrapper.site_adjusted_start_offset
        ):
            if isinstance(
                wrappers[key].unbundle_indicator(), _indicators.StartHairpin
            ) and isinstance(wrapper.unbundle_indicator(), _indicators.Dynamic):
                pass
            elif (
                getattr(wrapper.unbundle_indicator(), "spanner_start", False) is True
                or getattr(wrapper.unbundle_indicator(), "spanner_stop", False) is True
                or getattr(wrapper.unbundle_indicator(), "trend", False) is True
            ):
                wrappers[key] = wrapper
    return wrappers


def _get_sounding_pitch(note):
    if "sounding pitch" in note._get_indicators(str):
        return note.written_pitch
    else:
        instrument = _get_effective(note, _instruments.Instrument)
        if instrument:
            sounding_pitch = instrument.middle_c_sounding_pitch
        else:
            sounding_pitch = _pitch.NamedPitch("C4")
        interval = _pitch.NamedPitch("C4") - sounding_pitch
        sounding_pitch = interval.transpose(note.written_pitch)
        return sounding_pitch


def _get_sounding_pitches(chord):
    if "sounding pitch" in chord._get_indicators(str):
        return chord.written_pitches
    else:
        instrument = _get_effective(chord, _instruments.Instrument)
        if instrument:
            sounding_pitch = instrument.middle_c_sounding_pitch
        else:
            sounding_pitch = _pitch.NamedPitch("C4")
        interval = _pitch.NamedPitch("C4") - sounding_pitch
        sounding_pitches = [
            interval.transpose(pitch) for pitch in chord.written_pitches
        ]
        return tuple(sounding_pitches)


def _get_timespan(argument, in_seconds: bool = False):
    if isinstance(argument, _score.Component):
        return argument._get_timespan(in_seconds=in_seconds)
    assert isinstance(argument, collections.abc.Iterable), repr(argument)
    remaining_items = []
    for i, item in enumerate(argument):
        if i == 0:
            first_item = item
        else:
            remaining_items.append(item)
    timespan = _get_timespan(first_item, in_seconds=in_seconds)
    start_offset = timespan.start_offset
    stop_offset = timespan.stop_offset
    for item in remaining_items:
        timespan = _get_timespan(item, in_seconds=in_seconds)
        if timespan.start_offset < start_offset:
            start_offset = timespan.start_offset
        if stop_offset < timespan.stop_offset:
            stop_offset = timespan.stop_offset
    return _timespan.Timespan(start_offset, stop_offset)
