def _get_lilypond_command_mark_format_contributions_for_slot(component, slot):
    '''.. versionadded:: 2.0
    '''
    from abjad.tools import marktools

    result = []
    comment_marks = marktools.get_lilypond_command_marks_attached_to_component(component)
    for comment_mark in comment_marks:
        if comment_mark._format_slot == slot:
            result.append(comment_mark.format)
    return ['lilypond command marks', result]
