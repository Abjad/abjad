import bisect

from . import exceptions
from .duration import Duration
from .indicators.MetronomeMark import MetronomeMark
from .parentage import Parentage
from .score import Component, Container, Context, Voice


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


# def _get_logical_voice(component):
