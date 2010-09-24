from abjad import *


def test_BookpartBlock_01( ):

   bookpart_block = lilyfiletools.BookpartBlock( )
   
   r'''
   \bookpart { }
   '''

   assert bookpart_block.format == '\\bookpart { }'
