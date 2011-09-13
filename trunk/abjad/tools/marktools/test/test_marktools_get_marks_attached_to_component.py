from abjad import *


def test_marktools_get_marks_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.leaves)
    comment_mark = marktools.LilyPondComment('beginning of note content')(staff[0])
    lilypond_command_mark = marktools.LilyPondCommandMark('slurDotted')(staff[0])

    r'''
    \new Staff {
        %% beginning of note content
        \slurDotted
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    marks = marktools.get_marks_attached_to_component(staff[0])

    assert comment_mark in marks
    assert lilypond_command_mark in marks
    assert len(marks) == 2
