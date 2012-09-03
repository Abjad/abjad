from abjad import *


def test_markuptools_make_vertically_adjusted_composer_markup_01():

    markup = markuptools.make_vertically_adjusted_composer_markup('Josquin Desprez')

    r'''
    \markup {
        \override
            #'(font - name Times)
            {
                \hspace
                    #0
                \raise
                    #-20
                    \fontsize
                        #3
                        "Josquin Desprez"
                \hspace
                    #0
            }
        }
    '''

    assert markup.lilypond_format == '\\markup { \\override #\'(font - name Times) { \\hspace #0 \\raise #-20 \\fontsize #3 "Josquin Desprez" \\hspace #0 } }'
    assert markup.indented_lilypond_format == '\\markup {\n\t\\override\n\t\t#\'(font - name Times)\n\t\t{\n\t\t\t\\hspace\n\t\t\t\t#0\n\t\t\t\\raise\n\t\t\t\t#-20\n\t\t\t\t\\fontsize\n\t\t\t\t\t#3\n\t\t\t\t\t"Josquin Desprez"\n\t\t\t\\hspace\n\t\t\t\t#0\n\t\t}\n\t}'
