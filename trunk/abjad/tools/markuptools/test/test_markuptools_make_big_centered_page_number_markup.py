from abjad import *


def test_markuptools_make_big_centered_page_number_markup_01():

    markup = markuptools.make_big_centered_page_number_markup()

    r'''
    \markup {
        \fill-line {
        \bold \fontsize #3 \concat {
        \on-the-fly #print-page-number-check-first
        \fromproperty #'page:page-number-string } } }
    '''

    assert markup.format == "\\markup { \n        \\fill-line {\n        \\bold \\fontsize #3 \\concat {\n        \\on-the-fly #print-page-number-check-first\n        \\fromproperty #'page:page-number-string } } }"
