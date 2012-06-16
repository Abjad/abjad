from abjad import *


def test_markuptools_make_vertically_adjusted_composer_markup_01():

    markup = markuptools.make_vertically_adjusted_composer_markup('Josquin Desprez')

    r'''
    \markup { 
            \override #'(font-name . "Times")
            \hspace #0 \raise #-20
            \fontsize #3 "Josquin Desprez" \hspace #0
            }
    '''

    assert markup.lilypond_format == '\\markup { \n        \\override #\'(font-name . "Times")\n        \\hspace #0 \\raise #-20\n        \\fontsize #3 "Josquin Desprez" \\hspace #0\n        }'
