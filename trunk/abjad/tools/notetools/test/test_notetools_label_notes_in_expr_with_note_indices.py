from abjad import *


def test_notetools_label_notes_in_expr_with_note_indices_01():

    staff = Staff("c'8 d'8 r8 r8 g'8 a'8 r8 c''8")
    notetools.label_notes_in_expr_with_note_indices(staff)

    r'''
    \new Staff {
        c'8 _ \markup { \small 0 }
        d'8 _ \markup { \small 1 }
        r8
        r8
        g'8 _ \markup { \small 2 }
        a'8 _ \markup { \small 3 }
        r8
        c''8 _ \markup { \small 4 }
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 _ \\markup { \\small 0 }\n\td'8 _ \\markup { \\small 1 }\n\tr8\n\tr8\n\tg'8 _ \\markup { \\small 2 }\n\ta'8 _ \\markup { \\small 3 }\n\tr8\n\tc''8 _ \\markup { \\small 4 }\n}"
