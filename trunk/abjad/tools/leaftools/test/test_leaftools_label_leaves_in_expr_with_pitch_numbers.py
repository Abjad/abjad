from abjad import *


def test_labeltools_label_leaves_in_expr_with_pitch_numbers_01():
    '''Works on notes, rests and chords.
    '''

    leaves = leaftools.make_leaves([None, 12, (13, 14, 15), None], [(1, 4)])
    t = Staff(leaves)
    labeltools.label_leaves_in_expr_with_pitch_numbers(t)

    r'''
    \new Staff {
        r4
        c''4
            _ \markup {
                \small
                    12
                }
        <cs'' d'' ef''>4
            _ \markup {
                \column
                    {
                        \small
                            15
                        \small
                            14
                        \small
                            13
                    }
                }
        r4
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\tr4\n\tc''4\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t12\n\t\t\t}\n\t<cs'' d'' ef''>4\n\t\t_ \\markup {\n\t\t\t\\column\n\t\t\t\t{\n\t\t\t\t\t\\small\n\t\t\t\t\t\t15\n\t\t\t\t\t\\small\n\t\t\t\t\t\t14\n\t\t\t\t\t\\small\n\t\t\t\t\t\t13\n\t\t\t\t}\n\t\t\t}\n\tr4\n}"
