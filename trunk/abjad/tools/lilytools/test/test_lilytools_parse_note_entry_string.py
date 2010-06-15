from abjad import *


def test_lilytools_parse_note_entry_string_01( ):

   note_entry_string = r'''g'4 a'4 ~ a'2 \bar "||" g'4. fs'8 e'4 d'4 \fermata'''
   container = lilytools.parse_note_entry_string(note_entry_string)
   staff = Staff([ ])
   staff[:] = container[:]

   r'''
   \new Staff {
           g'4
           a'4 ~
           a'2
           \bar "||"
           g'4.
           fs'8
           e'4
           d'4 -\fermata
   }
   '''
   
   assert componenttools.is_well_formed_component(staff)
   assert staff.format == '\\new Staff {\n\tg\'4\n\ta\'4 ~\n\ta\'2\n\t\\bar "||"\n\tg\'4.\n\tfs\'8\n\te\'4\n\td\'4 -\\fermata\n}'
