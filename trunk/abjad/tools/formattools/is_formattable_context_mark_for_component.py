def is_formattable_context_mark_for_component(mark, component):
    '''Return True if ContextMark `mark` can format for `component`.''' 

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
                prev_measure = measuretools.get_previous_measure_from_component(
                    mark.start_component)
                if prev_measure is not None:
                    prev_effective_time_signature = \
                        contexttools.get_effective_time_signature(prev_measure)
                else:
                    prev_effective_time_signature = None
                if not mark == prev_effective_time_signature:
                    return True

    elif mark._format_slot == 'right':
        if mark.start_component is component:
            return True

    elif mark.start_component is component:
        return True

    else:
        improper_parentage = componenttools.get_improper_parentage_of_component(component)
        if mark.effective_context in improper_parentage:
            proper_parentage = componenttools.get_proper_parentage_of_component(component)
            if mark.effective_context not in proper_parentage:
                if mark.start_component.start == component.start:
                    return True

    return False
