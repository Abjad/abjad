def get_comment_format_contributions_for_slot(component, slot):
    '''.. versionadded:: 2.0
    
    Get comment format contributions for `component` at `slot`.

    Return list.
    '''
    from abjad.tools import marktools

    result = []
    comment_marks = marktools.get_lilypond_comments_attached_to_component(component)
    for comment_mark in comment_marks:
        if comment_mark._format_slot == slot:
            result.append(comment_mark.lilypond_format)
    return ['comments', result]

