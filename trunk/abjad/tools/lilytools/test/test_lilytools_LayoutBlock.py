from abjad import *


def test_lilytools_LayoutBlock_01( ):

   lb = lilytools.LayoutBlock( )
   lb.indent = 0
   lb.ragged_right = True

   r'''
   \layout {
           indent = #0
           ragged-right = ##t
   }
   '''

   assert lb.format == '\\layout {\n\tindent = #0\n\tragged-right = ##t\n}'
