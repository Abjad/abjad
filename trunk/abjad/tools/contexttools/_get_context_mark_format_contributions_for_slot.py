from abjad.tools import componenttools
from abjad.tools import measuretools


def _get_context_mark_format_contributions_for_slot(component, slot):
    from abjad.tools import contexttools

    result = []
    marks = set([])
    candidates = contexttools.get_context_marks_attached_to_any_improper_parent_of_component(
        component)
    #print candidates
    for candidate in candidates:
        if candidate._format_slot == slot:
            if candidate.start_component is not None:
                if isinstance(candidate.start_component, measuretools.Measure):
                    if candidate.start_component is component:
                        if not isinstance(candidate, contexttools.TimeSignatureMark):
                            marks.add(candidate)
                        elif component.always_format_time_signature:
                            marks.add(candidate)
                        else:
                            prev_measure = measuretools.get_previous_measure_from_component(candidate.start_component)
                            if prev_measure is not None:
                                prev_effective_time_signature = contexttools.get_effective_time_signature(
                                    prev_measure)
                            else:
                                prev_effective_time_signature = None
                            if not candidate == prev_effective_time_signature:
                                marks.add(candidate)
                elif candidate._format_slot == 'right':
                    if candidate.start_component is component:
                        marks.add(candidate)
                elif candidate.start_component is component:
                    marks.add(candidate)
                else:
                    improper_parentage = componenttools.get_improper_parentage_of_component(component)
                    if candidate.effective_context in improper_parentage:
                        proper_parentage = componenttools.get_proper_parentage_of_component(component)
                        if candidate.effective_context not in proper_parentage:
                            if candidate.start_component.start == component.start:
                                marks.add(candidate)
    #print marks
    for mark in marks:
        #print mark, mark.format
        addenda = []
        mark_format = mark.format
        if isinstance(mark_format, (tuple, list)):
            addenda.extend(mark_format)
        else:
            addenda.append(mark_format)
        # cosmetic mark is a hack to allow marks to format even without effective context;
        # currently used only in metric grid formatting
        if mark.effective_context is not None or \
            getattr(mark, '_is_cosmetic_mark', False) or \
            (isinstance(mark, contexttools.TimeSignatureMark) and
            isinstance(mark.start_component, measuretools.Measure)):
            result.extend(addenda)
        else:
            addenda = [r'%%% ' + addendum + r' %%%' for addendum in addenda]
            result.extend(addenda)
    #print result
    #print ''
    result.sort()
    return ['context marks', result]
