from abjad import *


def test_markup_big_centered_page_number_01( ):

   t = markup.big_centered_page_number( )

   r'''
   \markup { 
      \fill-line {
      \bold \fontsize #3 \concat {
      \on-the-fly #print-page-number-check-first
      \fromproperty #'page:page-number-string } } }
   '''
   
   assert t.format == "\\markup { \n   \\fill-line {\n   \\bold \\fontsize #3 \\concat {\n   \\on-the-fly #print-page-number-check-first\n   \\fromproperty #'page:page-number-string } } }"
