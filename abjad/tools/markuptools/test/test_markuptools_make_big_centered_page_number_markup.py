# -*- encoding: utf-8 -*-
from abjad import *


def test_markuptools_make_big_centered_page_number_markup_01():

    markup = markuptools.make_big_centered_page_number_markup()

    assert systemtools.TestManager.compare(
        format(markup, 'lilypond'),
        r'''
        \markup {
            \fill-line
                {
                    \bold
                        \fontsize
                            #3
                            \concat
                                {
                                    \on-the-fly
                                        #print-page-number-check-first
                                        \fromproperty
                                            #'page:page-number-string
                                }
                }
            }
        ''',
        )
