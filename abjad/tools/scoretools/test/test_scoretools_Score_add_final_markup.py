# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Score_add_final_markup_01():

    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    score = abjad.Score([staff])
    markup = r'\italic \right-column { "Bremen - Boston - Los Angeles." "Jul 2010 - May 2011." }'
    markup = abjad.Markup(markup, Down)
    score.add_final_markup(markup, extra_offset=(4, -2))


    r'''
    \new Score <<
        \new Staff {
            c'4
            d'4
            e'4
            \once \override TextScript.extra-offset = #'(4 . -2)
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

    assert format(score) == abjad.String.normalize(
        r'''
        \new Score <<
            \new Staff {
                c'4
                d'4
                e'4
                \once \override TextScript.extra-offset = #'(4 . -2)
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
        )
