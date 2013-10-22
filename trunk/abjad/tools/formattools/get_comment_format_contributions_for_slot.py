# -*- encoding: utf-8 -*-


def get_comment_format_contributions_for_slot(component, slot):
    '''Get comment format contributions for `component` at `slot`.

    Returns list.
    '''
    from abjad.tools import marktools

    result = []
    comment_marks = component._get_marks(marktools.LilyPondComment)
    for comment_mark in comment_marks:
        if comment_mark._format_slot == slot:
            result.append(comment_mark.lilypond_format)
    return ['comments', result]
