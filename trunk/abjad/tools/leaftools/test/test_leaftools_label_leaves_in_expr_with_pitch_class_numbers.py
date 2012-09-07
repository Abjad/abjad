from abjad import *


def test_labeltools_label_leaves_in_expr_with_pitch_class_numbers_01():
    '''With number = True.'''

    t = Staff("c'8 d'8 e'8 f'8")
    labeltools.label_leaves_in_expr_with_pitch_class_numbers(t, number=True)

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
                    2
                }
        e'8
            _ \markup {
                \small
                    4
                }
        f'8
            _ \markup {
                \small
                    5
                }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\tc'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t0\n\t\t\t}\n\td'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t2\n\t\t\t}\n\te'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t4\n\t\t\t}\n\tf'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t5\n\t\t\t}\n}"


def test_labeltools_label_leaves_in_expr_with_pitch_class_numbers_02():
    '''With color = True.'''

    t = Staff("c'8 d'8 e'8 f'8")
    labeltools.label_leaves_in_expr_with_pitch_class_numbers(t, number=False, color=True)

    r'''
    \new Staff {
      \once \override NoteHead #'color = #(x11-color 'red)
      c'8
      \once \override NoteHead #'color = #(x11-color 'orange)
      d'8
      \once \override NoteHead #'color = #(x11-color 'ForestGreen)
      e'8
      \once \override NoteHead #'color = #(x11-color 'MediumOrchid)
      f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\t\\once \\override NoteHead #'color = #(x11-color 'red)\n\tc'8\n\t\\once \\override NoteHead #'color = #(x11-color 'orange)\n\td'8\n\t\\once \\override NoteHead #'color = #(x11-color 'ForestGreen)\n\te'8\n\t\\once \\override NoteHead #'color = #(x11-color 'MediumOrchid)\n\tf'8\n}"
