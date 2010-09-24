from abjad import *


def test_lilyfiletools_HeaderBlock_01( ):

   header_block = lilyfiletools.HeaderBlock( )
   header_block.composer = markuptools.Markup('Josquin')
   header_block.title = markuptools.Markup('Missa sexti tonus')

   r'''
   \header {
           composer = \markup { Josquin }
           title = \markup { Missa sexti tonus }
   }
   '''

   assert header_block.format == '\\header {\n\tcomposer = \\markup { Josquin }\n\ttitle = \\markup { Missa sexti tonus }\n}'
