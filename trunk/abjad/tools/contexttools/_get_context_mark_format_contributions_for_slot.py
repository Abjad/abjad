def _get_context_mark_format_contributions_for_slot(component, slot):
    from abjad.tools.leaftools._Leaf import _Leaf
    from abjad.tools.measuretools.Measure import Measure
    from abjad.tools import componenttools
    from abjad.tools import contexttools
    from abjad.tools.contexttools.TimeSignatureMark import TimeSignatureMark

    result = []
    marks = set([])
    candidates = contexttools.get_context_marks_attached_to_any_improper_parent_of_component(
        component)
    #print candidates
    for candidate in candidates:
        if candidate._format_slot == slot:
            if candidate.start_component is not None:
                if isinstance(candidate.start_component, Measure):
                    if candidate.start_component is component:
                        marks.add(candidate)
                elif candidate._format_slot == 'right':
                    if candidate.start_component is component:
                        marks.add(candidate)
                elif candidate.start_component is component:
                    if candidate.effective_context is None:
                        marks.add(candidate)
                    elif candidate.effective_context is component:
                        marks.add(candidate)
                    elif candidate.effective_context._offset.start < \
                        candidate.start_component._offset.start:
                        marks.add(candidate)
                else:
                    improper_parentage = componenttools.get_improper_parentage_of_component(component)
                    if candidate.effective_context in improper_parentage:
                        proper_parentage = componenttools.get_proper_parentage_of_component(component)
                        if candidate.effective_context not in proper_parentage:
                            if candidate.start_component._offset.start == component._offset.start:
                                marks.add(candidate)
    #print marks
    for mark in marks:
        #print mark, mark.format
        addenda = []
        mark_format = mark.format
        if isinstance(mark_format, (tuple, list)):
            #result.extend(mark_format)
            addenda.extend(mark_format)
        else:
            #result.append(mark_format)
            addenda.append(mark_format)
        # cosmetic mark is a hack to allow marks to format even without effective context;
        # currently used only in metric grid formatting
        if mark.effective_context is not None or \
            getattr(mark, '_is_cosmetic_mark', False) or \
            (isinstance(mark, TimeSignatureMark) and
            isinstance(mark.start_component, Measure)):
            result.extend(addenda)
        else:
            addenda = [r'%%% ' + addendum + r' %%%' for addendum in addenda]
            result.extend(addenda)
    #print result
    #print ''
    result.sort()
    return ['context marks', result]
