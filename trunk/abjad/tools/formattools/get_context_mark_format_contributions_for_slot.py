from abjad.tools.formattools.get_context_mark_format_pieces import get_context_mark_format_pieces
from abjad.tools.formattools.is_formattable_context_mark_for_component import is_formattable_context_mark_for_component


def get_context_mark_format_contributions_for_slot(component, slot):
    r'''.. versionadded:: 2.0

    Get context mark format contributions for `component` at `slot`.

    Return list.
    '''
    from abjad.tools import componenttools
    from abjad.tools import contexttools
    from abjad.tools import measuretools

    result = []
    marks = set([])
    candidates = contexttools.get_context_marks_attached_to_any_improper_parent_of_component(
        component)

    for candidate in candidates:
        if candidate._format_slot == slot:
            if is_formattable_context_mark_for_component(candidate, component):
                marks.add(candidate)

    for mark in marks:
        result.extend(get_context_mark_format_pieces(mark))

    result.sort()
    return ['context marks', result]
