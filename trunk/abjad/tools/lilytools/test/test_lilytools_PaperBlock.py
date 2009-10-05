from abjad import *


def test_lilytools_PaperBlock_01( ):

   pb = lilytools.PaperBlock( )
   pb.top_margin = 15
   pb.left_margin = 15

   r'''
   \paper {
           left-margin = #15
           top-margin = #15
   }
   '''

   assert pb.format == '\\paper {\n\tleft-margin = #15\n\ttop-margin = #15\n}'
