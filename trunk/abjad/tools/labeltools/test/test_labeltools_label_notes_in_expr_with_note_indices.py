from abjad import *


def test_labeltools_label_notes_in_expr_with_note_indices_01():

    staff = Staff("c'8 d'8 r8 r8 g'8 a'8 r8 c''8")
    labeltools.label_notes_in_expr_with_note_indices(staff)

    r'''
    \new Staff {
        c'8
            _ \markup {
                \small
                    0
                }
        d'8
            _ \markup {
                \small
                    1
                }
        r8
        r8
        g'8
            _ \markup {
                \small
                    2
                }
        a'8
            _ \markup {
                \small
                    3
                }
        r8
        c''8
            _ \markup {
                \small
                    4
                }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tc'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t0\n\t\t\t}\n\td'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t1\n\t\t\t}\n\tr8\n\tr8\n\tg'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t2\n\t\t\t}\n\ta'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t3\n\t\t\t}\n\tr8\n\tc''8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t4\n\t\t\t}\n}"

