# -*- encoding: utf-8 -*-


def is_formattable_context_mark_for_component(mark, component):
    r'''Return True if ContextMark `mark` can format for `component`.
    '''
    from abjad.tools import componenttools
    from abjad.tools import contexttools
    from abjad.tools import measuretools

    if mark.start_component is None:
        return False

    if isinstance(mark.start_component, measuretools.Measure):
        if mark.start_component is component:
            if not isinstance(mark, contexttools.TimeSignatureMark):
                return True
            elif component.always_format_time_signature:
                return True
            else:
                previous_measure = \
                    measuretools.get_previous_measure_from_component(
                    mark.start_component)
                if previous_measure is not None:
                    previous_effective_time_signature = \
                        previous_measure.time_signature
                else:
                    previous_effective_time_signature = None
                if not mark == previous_effective_time_signature:
                    return True

    elif mark._format_slot == 'right':
        if mark.start_component is component:
            return True

    elif mark.start_component is component:
        return True

    else:
        if mark.effective_context in \
            component._get_parentage(include_self=True):
            if mark.effective_context not in \
                component._get_parentage(include_self=False):
                if mark.start_component.start == component.start:
                    return True

    return False
