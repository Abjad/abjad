from abjad import *


def test_lilypondfiletools_make_basic_lily_file_01():


    score = Score([Staff("c'8 d'8 e'8 f'8")])
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    lilypond_file.header_block.composer = markuptools.Markup('Josquin')
    lilypond_file.layout_block.indent = 0
    lilypond_file.paper_block.top_margin = 15
    lilypond_file.paper_block.left_margin = 15

    lilypond_file.file_initial_system_comments = []
    lilypond_file.file_initial_system_includes = []

    r'''
    \header {
        composer = \markup { Josquin }
    }

    \layout {
        indent = #0
    }

    \paper {
        left-margin = #15
        top-margin = #15
    }

    \score {
        \new Score <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
        >>
    }
    '''

    assert score.lilypond_file is lilypond_file
    assert lilypond_file.score_block[0] is score

    assert lilypond_file.format == "\\header {\n\tcomposer = \\markup { Josquin }\n}\n\n\\layout {\n\tindent = #0\n}\n\n\\paper {\n\tleft-margin = #15\n\ttop-margin = #15\n}\n\n\\score {\n\t\\new Score <<\n\t\t\\new Staff {\n\t\t\tc'8\n\t\t\td'8\n\t\t\te'8\n\t\t\tf'8\n\t\t}\n\t>>\n}"
