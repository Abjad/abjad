# -*- encoding: utf-8 -*-


def get_lilypond_command_mark_format_contributions_for_slot(component, slot):
    '''Get LilyPond command mark format contributions for `component` at `slot`.

    Returns list.
    '''
    from abjad.tools import marktools

    result = []
    command_marks = component._get_marks(marktools.LilyPondCommandMark)
    for command_mark in command_marks:
        if command_mark._format_slot == slot:
            result.append(command_mark.lilypond_format)
    return ['lilypond command marks', result]
