from abjad import *


def test_lilytools_BookBlock_01( ):

   book_block = lilytools.BookBlock( )
   
   r'''
   \book { }
   '''

   assert book_block.format == '\\book { }'
