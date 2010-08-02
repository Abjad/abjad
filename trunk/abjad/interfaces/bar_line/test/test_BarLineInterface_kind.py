from abjad import *


def test_bar_line_interface_kind_01( ):
   '''Barline after leaf.'''

   t = Note(0, (1, 4))
   t.bar_line.kind = '|.'

   r'''
   c'4
   \bar "|."
   '''

   assert t.format == 'c\'4\n\\bar "|."'


def test_bar_line_interface_kind_02( ):
   '''Barline at container closing.'''

   t = Staff( )
   t.bar_line.kind = '|.'

   r'''
   \new Staff {
           \bar "|."
   }
   '''

   assert t.format == '\\new Staff {\n\t\\bar "|."\n}' 


def test_bar_line_interface_kind_03( ):
   '''Empty LilyPond bar line string.'''

   t = Staff(macros.scale(4))
   t[0].bar_line.kind = ''

   r'''
   \new Staff {
      c'8
      \bar ""
      d'8
      e'8
      f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\new Staff {\n\tc\'8\n\t\\bar ""\n\td\'8\n\te\'8\n\tf\'8\n}'
