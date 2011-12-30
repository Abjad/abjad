from abjad import *


def test_marktools_get_lilypond_command_marks_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.leaves)
    lilypond_command_mark_1 = marktools.LilyPondCommandMark('slurDotted')(staff[0])
    lilypond_command_mark_2 = marktools.LilyPondCommandMark('slurUp')(staff[0])

    r'''
    \new Staff {
        \slurDotted
        \slurUp
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    marks = marktools.get_lilypond_command_marks_attached_to_component(staff[0])

    assert lilypond_command_mark_1 in marks
    assert lilypond_command_mark_2 in marks
    assert len(marks) == 2


def test_marktools_get_lilypond_command_marks_attached_to_component_02():
    '''Get LilyPond command marks with command name.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.leaves)
    lilypond_command_mark_1 = marktools.LilyPondCommandMark('slurDotted')(staff[0])
    lilypond_command_mark_2 = marktools.LilyPondCommandMark('slurUp')(staff[0])

    r'''
    \new Staff {
        \slurDotted
        \slurUp
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    marks = marktools.get_lilypond_command_marks_attached_to_component(staff[0], 'slurDotted')

    assert lilypond_command_mark_1 in marks
    assert len(marks) == 1
