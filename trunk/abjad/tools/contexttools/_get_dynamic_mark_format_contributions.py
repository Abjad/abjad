def _get_dynamic_mark_format_contributions(component):
    '''.. versionadded:: 2.0
    '''
    from abjad.tools import contexttools

    result = []
    dynamic_marks = contexttools.get_dynamic_marks_attached_to_component(component)
    for dynamic_mark in dynamic_marks:
        result.append(dynamic_mark.format)
    result.sort()
    return result
