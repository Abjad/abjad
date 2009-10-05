from abjad import *


def test_lilytools_BookpartBlock_01( ):

   bookpart_block = lilytools.BookpartBlock( )
   
   r'''
   \bookpart { }
   '''

   assert bookpart_block.format == '\\bookpart { }'
