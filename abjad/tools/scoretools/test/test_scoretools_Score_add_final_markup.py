# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Score_add_final_markup_01():

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

    assert format(score) == stringtools.normalize(
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
