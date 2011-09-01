from abjad import *
import py.test


def test_LilyPondCommandMark___init___01():
    '''Initialize LilyPond command mark from command name.
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


def test_LilyPondCommandMark___init___02():
    '''Set LilyPond command mark from command name.
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


def test_LilyPondCommandMark___init___03():
    '''Initialize LilyPond command mark from string and format slot.
    '''

    lilypond_command_mark = marktools.LilyPondCommandMark('break', 'closing')
    assert isinstance(lilypond_command_mark, marktools.LilyPondCommandMark)


def test_LilyPondCommandMark___init___04():
    '''Initialize LilyPondCommand mark from other LilyPond command mark.
    '''

    lilypond_command_mark_1 = marktools.LilyPondCommandMark('break', 'closing')
    lilypond_command_mark_2 = marktools.LilyPondCommandMark(lilypond_command_mark_1)

    assert isinstance(lilypond_command_mark_1, marktools.LilyPondCommandMark)
    assert isinstance(lilypond_command_mark_2, marktools.LilyPondCommandMark)
    assert lilypond_command_mark_1 == lilypond_command_mark_2
    assert lilypond_command_mark_1 is not lilypond_command_mark_2
