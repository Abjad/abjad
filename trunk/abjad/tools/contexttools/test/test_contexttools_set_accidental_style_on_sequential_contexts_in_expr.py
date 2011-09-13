from abjad import *


def test_contexttools_set_accidental_style_on_sequential_contexts_in_expr_01():

    score = Score(Staff("c'8 d'8") * 2)
    contexttools.set_accidental_style_on_sequential_contexts_in_expr(score, 'forget')

    r'''
    \new Score <<
        \new Staff {
            #(set-accidental-style 'forget)
            c'8
            d'8
        }
        \new Staff {
            #(set-accidental-style 'forget)
            c'8
            d'8
        }
    >>
    '''

    assert componenttools.is_well_formed_component(score)
    assert score.format == "\\new Score <<\n\t\\new Staff {\n\t\t#(set-accidental-style 'forget)\n\t\tc'8\n\t\td'8\n\t}\n\t\\new Staff {\n\t\t#(set-accidental-style 'forget)\n\t\tc'8\n\t\td'8\n\t}\n>>"


def test_contexttools_set_accidental_style_on_sequential_contexts_in_expr_02():
    '''Skip nonsemantic contexts.
    '''

    score = Score(Staff("c'8 d'8") * 2)
    score[0].is_nonsemantic = True
    contexttools.set_accidental_style_on_sequential_contexts_in_expr(score, 'forget')

    r'''
    \new Score <<
        \new Staff {
            c'8
            d'8
        }
        \new Staff {
            #(set-accidental-style 'forget)
            c'8
            d'8
        }
    >>
    '''

    assert score.format == "\\new Score <<\n\t\\new Staff {\n\t\tc'8\n\t\td'8\n\t}\n\t\\new Staff {\n\t\t#(set-accidental-style 'forget)\n\t\tc'8\n\t\td'8\n\t}\n>>"
