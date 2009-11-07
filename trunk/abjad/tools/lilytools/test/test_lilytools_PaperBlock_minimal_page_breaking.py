from abjad import *


def test_lilytools_PaperBlock_minimal_page_breaking_01( ):

   pb = lilytools.PaperBlock( )
   pb.minimal_page_breaking = True

   r'''
   \paper {
           #(define page-breaking ly:minimal-breaking)
   }
   '''

   assert pb.format == '\\paper {\n\t#(define page-breaking ly:minimal-breaking)\n}'
