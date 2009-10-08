from abjad import *


def test_barline_interface_01( ):
   '''Barline after leaf.'''

   t = Note(0, (1, 4))
   t.barline.kind = '|.'

   r'''c'4
      \bar "|."
   '''

   assert t.format == 'c\'4\n\\bar "|."'


def test_barline_interface_02( ):
   '''Barline at container closing.'''

   t = Staff( )
   t.barline.kind = '|.'

   r'''\new Staff {
           \bar "|."
   }'''

   assert t.format == '\\new Staff {\n\t\\bar "|."\n}' 
