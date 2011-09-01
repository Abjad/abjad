from abjad import *


def test_marktools_attach_lilypond_command_marks_to_components_in_expr_01( ):

    staff = Staff("c'8 d'8 e'8 f'8")
    lilypond_command_mark = marktools.LilyPondCommandMark('stemUp')
    marktools.attach_lilypond_command_marks_to_components_in_expr(
        staff.leaves, [lilypond_command_mark])

    r'''
    \new Staff {
        \stemUp
        c'8
        \stemUp
        d'8
        \stemUp
        e'8
        \stemUp
        f'8
    }
    '''

    for leaf in staff.leaves:
        new_lilypond_command_mark = \
            marktools.get_lilypond_command_marks_attached_to_component(leaf)[0] 
        assert new_lilypond_command_mark == lilypond_command_mark
        assert new_lilypond_command_mark is not lilypond_command_mark

    assert staff.format == "\\new Staff {\n\t\\stemUp\n\tc'8\n\t\\stemUp\n\td'8\n\t\\stemUp\n\te'8\n\t\\stemUp\n\tf'8\n}"
