from abjad import *
import py.test


def test_LilyPondCommandMark___init___01( ):
    '''Initialize LilyPond \slurDotted command.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.leaves)
    lilypond_command = marktools.LilyPondCommandMark(r'slurDotted')(staff[0])


    r'''
    \new Staff {
        \slurDotted
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\t\\slurDotted\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"


def test_LilyPondCommandMark___init___02( ):
    '''Set LilyPond \slurUp command.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.leaves)
    lilypond_command = marktools.LilyPondCommandMark(r'slurUp')(staff[0])


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

