from abjad import *


def test_Score_add_final_markup_01():

    staff = Staff("c'4 d'4 e'4 f'4")
    score = Score([staff])
    markup = r'\italic \right-column { "Bremen - Boston - Los Angeles." "Jul 2010 - May 2011." }'
    markup = markuptools.Markup(markup, Down)
    score.add_final_markup(markup, extra_offset=(4, -2))
    

    r'''
    \new Score <<
        \new Staff {
            c'4
            d'4
            e'4
            \once \override TextScript #'extra-offset = #'(4 . -2)
            f'4
                _ \markup {
                    \italic
                        \right-column
                            {
                                "Bremen - Boston - Los Angeles."
                                "Jul 2010 - May 2011."
                            }
                    }
        }
    >>
    '''

    assert score.lilypond_format == '\\new Score <<\n\t\\new Staff {\n\t\tc\'4\n\t\td\'4\n\t\te\'4\n\t\t\\once \\override TextScript #\'extra-offset = #\'(4 . -2)\n\t\tf\'4\n\t\t\t_ \\markup {\n\t\t\t\t\\italic\n\t\t\t\t\t\\right-column\n\t\t\t\t\t\t{\n\t\t\t\t\t\t\t"Bremen - Boston - Los Angeles."\n\t\t\t\t\t\t\t"Jul 2010 - May 2011."\n\t\t\t\t\t\t}\n\t\t\t\t}\n\t}\n>>'
