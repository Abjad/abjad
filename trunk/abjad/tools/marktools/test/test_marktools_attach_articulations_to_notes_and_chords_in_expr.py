from abjad import *


def test_marktools_attach_articulations_to_notes_and_chords_in_expr_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    marktools.attach_articulations_to_notes_and_chords_in_expr(staff, list('^.'))

    r'''
    \new Staff {
        c'8 -\marcato -\staccato
        d'8 -\marcato -\staccato
        e'8 -\marcato -\staccato
        f'8 -\marcato -\staccato
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 -\\marcato -\\staccato\n\td'8 -\\marcato -\\staccato\n\te'8 -\\marcato -\\staccato\n\tf'8 -\\marcato -\\staccato\n}"
