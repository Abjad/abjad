import bisect
import collections
import typing

from . import exceptions, typings
from .duration import Duration
from .indicators.MetronomeMark import MetronomeMark
from .instruments import Instrument
from .parentage import Parentage
from .pitch.pitches import NamedPitch
from .score import (
    AfterGraceContainer,
    BeforeGraceContainer,
    Component,
    Container,
    Context,
    Leaf,
    Voice,
)
from .timespan import Timespan


def _are_logical_voice(COMPONENTS, prototype=None):
    prototype = prototype or (Component,)
    if not isinstance(prototype, tuple):
        prototype = (prototype,)
    assert isinstance(prototype, tuple)
    if len(COMPONENTS) == 0:
        return True
    if all(isinstance(_, prototype) and _._parent is None for _ in COMPONENTS):
        return True
    first = COMPONENTS[0]
    if not isinstance(first, prototype):
        return False
    same_logical_voice = True
    parentage = Parentage(first)
    first_logical_voice = parentage.logical_voice()
    for component in COMPONENTS[1:]:
        parentage = Parentage(component)
        if parentage.logical_voice() != first_logical_voice:
            same_logical_voice = False
        if not parentage.orphan and not same_logical_voice:
            return False
    return True


def _get_annotation(COMPONENT, annotation, default=None, unwrap: bool = True):
    assert isinstance(annotation, str), repr(annotation)
    for wrapper in _get_annotation_wrappers(COMPONENT):
        if wrapper.annotation == annotation:
            if unwrap is True:
                return wrapper.indicator
            else:
                return wrapper
    return default


def _get_annotation_wrappers(ARGUMENT):
    result = []
    for wrapper in getattr(ARGUMENT, "_wrappers", []):
        if wrapper.annotation:
            result.append(wrapper)
    return result


def _get_duration(ARGUMENT, in_seconds: bool = None):
    if isinstance(ARGUMENT, Component):
        if in_seconds is True:
            return _get_duration_in_seconds(ARGUMENT)
        else:
            return ARGUMENT._get_duration()
    assert isinstance(ARGUMENT, collections.abc.Iterable), repr(ARGUMENT)
    durations = [_get_duration(_, in_seconds=in_seconds) for _ in ARGUMENT]
    return Duration(sum(durations))


def _get_duration_in_seconds(COMPONENT):
    if isinstance(COMPONENT, Container):
        if COMPONENT.simultaneous:
            return max([Duration(0)] + [_get_duration_in_seconds(_) for _ in COMPONENT])
        else:
            duration = Duration(0)
            for component in COMPONENT:
                duration += _get_duration_in_seconds(component)
            return duration
    else:
        mark = _get_effective(COMPONENT, MetronomeMark)
        if mark is not None and not mark.is_imprecise:
            result = (
                COMPONENT._get_duration()
                / mark.reference_duration
                / mark.units_per_minute
                * 60
            )
            return Duration(result)
        raise exceptions.MissingMetronomeMarkError


def _get_effective(
    COMPONENT, prototype, *, attributes=None, command=None, n=0, unwrap=True
):
    COMPONENT._update_now(indicators=True)
    candidate_wrappers = {}
    parentage = COMPONENT._get_parentage()
    enclosing_voice_name = None
    for component in parentage:
        if isinstance(component, Voice):
            if (
                enclosing_voice_name is not None
                and component.name != enclosing_voice_name
            ):
                continue
            else:
                enclosing_voice_name = component.name or id(component)
        local_wrappers = []
        for wrapper in component._wrappers:
            if wrapper.annotation:
                continue
            if isinstance(wrapper.indicator, prototype):
                append_wrapper = True
                if command is not None and wrapper.indicator.command != command:
                    continue
                if attributes is not None:
                    for name, value in attributes.items():
                        if getattr(wrapper.indicator, name, None) != value:
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
        if not isinstance(component, Context):
            continue
        for wrapper in component._dependent_wrappers:
            if wrapper.annotation:
                continue
            if isinstance(wrapper.indicator, prototype):
                append_wrapper = True
                if command is not None and wrapper.indicator.command != command:
                    continue
                if attributes is not None:
                    for name, value in attributes.items():
                        if getattr(wrapper.indicator, name, None) != value:
                            append_wrapper = False
                if not append_wrapper:
                    continue
                offset = wrapper.start_offset
                candidate_wrappers.setdefault(offset, []).append(wrapper)
    if not candidate_wrappers:
        return
    all_offsets = sorted(candidate_wrappers)
    start_offset = COMPONENT._get_timespan().start_offset
    index = bisect.bisect(all_offsets, start_offset) - 1 + int(n)
    if index < 0:
        return
    elif len(candidate_wrappers) <= index:
        return
    wrapper = candidate_wrappers[all_offsets[index]][0]
    if unwrap:
        return wrapper.indicator
    return wrapper


def _get_grace_container(COMPONENT):
    prototype = (
        AfterGraceContainer,
        BeforeGraceContainer,
    )
    for component in COMPONENT._get_parentage():
        if isinstance(component, prototype):
            return True
        if component.__class__.__name__ == "OnBeatGraceContainer":
            return True
    return False


def _get_indicator(
    COMPONENT,
    prototype: typings.Prototype = None,
    *,
    default: typing.Any = None,
    unwrap: bool = True,
) -> typing.Any:
    if not isinstance(COMPONENT, Component):
        raise Exception("can only get indicator on component.")
    indicators = COMPONENT._get_indicators(prototype=prototype, unwrap=unwrap)
    if not indicators:
        return default
    elif len(indicators) == 1:
        return list(indicators)[0]
    else:
        raise Exception("multiple indicators attached to component.")


def _get_leaf_from_leaf(LEAF, n):
    assert n in (-1, 0, 1), repr(n)
    if n == 0:
        return LEAF
    sibling = LEAF._sibling(n)
    if sibling is None:
        return None
    if n == 1:
        components = sibling._get_descendants_starting_with()
    else:
        assert n == -1
        if (
            isinstance(sibling, Container)
            and len(sibling) == 2
            and any(hasattr(_, "_leaf_duration") for _ in sibling)
        ):
            if sibling[0].__class__.__name__ == "OnBeatGraceContainer":
                main_voice = sibling[1]
            else:
                main_voice = sibling[0]
            return main_voice[-1]
        components = sibling._get_descendants_stopping_with()
    for component in components:
        if not isinstance(component, Leaf):
            continue
        if _are_logical_voice([LEAF, component]):
            return component


def _get_on_beat_anchor_voice(CONTAINER):
    container = CONTAINER._parent
    if container is None:
        return None
    if not container.simultaneous:
        return None
    if not len(container) == 2:
        return None
    index = container.index(CONTAINER)
    if index == 0 and container[1].__class__.__name__ == "OnBeatGraceContainer":
        return container[1]
    if index == 1 and container[0].__class__.__name__ == "OnBeatGraceContainer":
        return container[0]
    return None


def _get_persistent_wrappers(*, dependent_wrappers=None, omit_with_indicator=None):
    wrappers = {}
    for wrapper in dependent_wrappers:
        if wrapper.annotation:
            continue
        indicator = wrapper.indicator
        if not getattr(indicator, "persistent", False):
            continue
        assert isinstance(indicator.persistent, bool)
        should_omit = False
        if omit_with_indicator is not None:
            for component in wrapper.component._get_parentage():
                if component._has_indicator(omit_with_indicator):
                    should_omit = True
                    continue
        if should_omit:
            continue
        if hasattr(indicator, "parameter"):
            key = indicator.parameter
        elif isinstance(indicator, Instrument):
            key = "Instrument"
        else:
            key = str(type(indicator))
        if key not in wrappers or wrappers[key].start_offset <= wrapper.start_offset:
            wrappers[key] = wrapper
    return wrappers


def _get_sibling_with_graces(COMPONENT, n):
    assert n in (-1, 0, 1), repr(COMPONENT, n)
    if n == 0:
        return COMPONENT
    if COMPONENT._parent is None:
        return None
    if COMPONENT._parent.simultaneous:
        return None
    if (
        n == 1
        and getattr(COMPONENT._parent, "_main_leaf", None)
        and COMPONENT._parent._main_leaf._before_grace_container is COMPONENT._parent
        and COMPONENT is COMPONENT._parent[-1]
    ):
        return COMPONENT._parent._main_leaf
    # last leaf in on-beat grace redo
    if (
        n == 1
        and COMPONENT is COMPONENT._parent[-1]
        and COMPONENT._parent.__class__.__name__ == "OnBeatGraceContainer"
    ):
        return COMPONENT._parent._get_on_beat_anchor_leaf()
    if (
        n == 1
        and getattr(COMPONENT._parent, "_main_leaf", None)
        and COMPONENT._parent._main_leaf._after_grace_container is COMPONENT._parent
        and COMPONENT is COMPONENT._parent[-1]
    ):
        main_leaf = COMPONENT._parent._main_leaf
        if main_leaf is main_leaf._parent[-1]:
            return None
        index = main_leaf._parent.index(main_leaf)
        return main_leaf._parent[index + 1]
    if n == 1 and getattr(COMPONENT, "_after_grace_container", None):
        return COMPONENT._after_grace_container[0]
    if (
        n == -1
        and getattr(COMPONENT._parent, "_main_leaf", None)
        and COMPONENT._parent._main_leaf._after_grace_container is COMPONENT._parent
        and COMPONENT is COMPONENT._parent[0]
    ):
        return COMPONENT._parent._main_leaf
    if (
        n == -1
        and getattr(COMPONENT._parent, "_main_leaf", None)
        and COMPONENT._parent._main_leaf._before_grace_container is COMPONENT._parent
        and COMPONENT is COMPONENT._parent[0]
    ):
        main_leaf = COMPONENT._parent._main_leaf
        if main_leaf is main_leaf._parent[0]:
            return None
        index = main_leaf._parent.index(main_leaf)
        return main_leaf._parent[index - 1]
    # COMPONENT is main leaf in main voice (simultaneous with on-beat graces)
    if (
        n == -1
        and COMPONENT is COMPONENT._parent[0]
        and _get_on_beat_anchor_voice(COMPONENT._parent) is not None
    ):
        on_beat = _get_on_beat_anchor_voice(COMPONENT._parent)
        return on_beat[-1]
    if n == -1 and hasattr(COMPONENT, "_get_on_beat_anchor_voice"):
        raise Exception(repr(COMPONENT))
        on_beat = _get_on_beat_anchor_voice(COMPONENT)
        if on_beat is not None:
            return on_beat[-1]
    if n == -1 and getattr(COMPONENT, "_before_grace_container", None):
        return COMPONENT._before_grace_container[-1]
    index = COMPONENT._parent.index(COMPONENT) + n
    if not (0 <= index < len(COMPONENT._parent)):
        return None
    candidate = COMPONENT._parent[index]
    if n == 1 and getattr(candidate, "_before_grace_container", None):
        return candidate._before_grace_container[0]
    if n == -1 and getattr(candidate, "_after_grace_container", None):
        return candidate._after_grace_container[-1]
    return candidate


def _get_sounding_pitch(NOTE):
    if "sounding pitch" in NOTE._get_indicators(str):
        return NOTE.written_pitch
    else:
        instrument = _get_effective(NOTE, Instrument)
        if instrument:
            sounding_pitch = instrument.middle_c_sounding_pitch
        else:
            sounding_pitch = NamedPitch("C4")
        interval = NamedPitch("C4") - sounding_pitch
        sounding_pitch = interval.transpose(NOTE.written_pitch)
        return sounding_pitch


def _get_sounding_pitches(chord):
    if "sounding pitch" in chord._get_indicators(str):
        return chord.written_pitches
    else:
        instrument = _get_effective(chord, Instrument)
        if instrument:
            sounding_pitch = instrument.middle_c_sounding_pitch
        else:
            sounding_pitch = NamedPitch("C4")
        interval = NamedPitch("C4") - sounding_pitch
        sounding_pitches = [
            interval.transpose(pitch) for pitch in chord.written_pitches
        ]
        return tuple(sounding_pitches)


def _get_timespan(ARGUMENT, in_seconds: bool = False):
    if isinstance(ARGUMENT, Component):
        return ARGUMENT._get_timespan(in_seconds=in_seconds)
    assert isinstance(ARGUMENT, collections.abc.Iterable), repr(ARGUMENT)
    remaining_items = []
    for i, item in enumerate(ARGUMENT):
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
    return Timespan(start_offset, stop_offset)
