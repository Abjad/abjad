from abjad import *


def test_markuptools_make_big_centered_page_number_markup_01():

    markup = markuptools.make_big_centered_page_number_markup()

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
    '''

    assert markup.indented_lilypond_format == "\\markup {\n\t\\fill-line\n\t\t{\n\t\t\t\\bold\n\t\t\t\t\\fontsize\n\t\t\t\t\t#3\n\t\t\t\t\t\\concat\n\t\t\t\t\t\t{\n\t\t\t\t\t\t\t\\on-the-fly\n\t\t\t\t\t\t\t\t#print-page-number-check-first\n\t\t\t\t\t\t\t\t\\fromproperty\n\t\t\t\t\t\t\t\t\t#'page:page-number-string\n\t\t\t\t\t\t}\n\t\t}\n\t}"
