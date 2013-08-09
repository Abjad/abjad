# -*- encoding: utf-8 -*-
from abjad.tools.formattools.get_context_mark_format_pieces \
	import get_context_mark_format_pieces
from abjad.tools.formattools.is_formattable_context_mark_for_component \
	import is_formattable_context_mark_for_component


def get_context_mark_format_contributions_for_slot(component, slot):
    r'''Get context mark format contributions for `component` at `slot`.

    Return list.
    '''
    from abjad.tools import componenttools
    from abjad.tools import contexttools
    from abjad.tools import measuretools

    result = []
    marks = set([])
    parentage = component._select_parentage(include_self=True)
    candidates = parentage._get_marks(
        mark_classes=contexttools.ContextMark,
        recurse=False,
        )

    for candidate in candidates:
        if candidate._format_slot == slot:
            if is_formattable_context_mark_for_component(candidate, component):
                marks.add(candidate)

    for mark in marks:
        result.extend(get_context_mark_format_pieces(mark))

    result.sort()
    return ['context marks', result]
