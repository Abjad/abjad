from abjad import *


def test_marktools_detach_lilypond_command_marks_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.leaves)
    marktools.LilyPondCommandMark('slurDotted')(staff[0])
    marktools.LilyPondCommandMark('slurUp')(staff[0])

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

    marktools.detach_lilypond_command_marks_attached_to_component(staff[0])

    r'''
    \new Staff {
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"


def test_marktools_detach_lilypond_command_marks_attached_to_component_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.leaves)
    marktools.LilyPondCommandMark('slurDotted')(staff[0])
    marktools.LilyPondCommandMark('slurUp')(staff[0])

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

    marktools.detach_lilypond_command_marks_attached_to_component(staff[0], 'slurDotted')

    r'''
    \new Staff {
        \slurUp
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\t\\slurUp\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"
