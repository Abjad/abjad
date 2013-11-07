# -*- encoding: utf-8 -*-
from abjad import *


def test_markuptools_make_vertically_adjusted_composer_markup_01():

    markup = markuptools.make_vertically_adjusted_composer_markup(
        'Josquin Desprez')

    assert testtools.compare(
        markup.indented_lilypond_format,
        r'''
        \markup {
            \override
                #'(font-name . "Times")
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
        )

    assert format(markup, 'lilypond') == '\\markup { \\override #\'(font-name . "Times") { \\hspace #0 \\raise #-20 \\fontsize #3 "Josquin Desprez" \\hspace #0 } }'
