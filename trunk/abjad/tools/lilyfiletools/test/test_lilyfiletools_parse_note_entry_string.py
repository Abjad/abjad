from abjad import *


def test_lilyfiletools_parse_note_entry_string_01( ):

   note_entry_string = r'''g'4 a'4 ~ a'2 \bar "||" g'4. fs'8 e'4 d'4 \fermata'''
   container = lilyfiletools.parse_note_entry_string(note_entry_string)
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


def test_lilyfiletools_parse_note_entry_string_02( ):

   note_entry_string = r'''c'4 g'4 b8 c'8 d'8 -. ( ef'8 ^\marcato <bf cs' f'>4 c'4 )'''
   container = lilyfiletools.parse_note_entry_string(note_entry_string)
   staff = Staff([ ])
   staff[:] = container[:]

   r'''
   \new Staff {
           c'4
           g'4
           b8
           c'8
           d'8 -\staccato (
           ef'8 ^\marcato
           <bf cs' f'>4
           c'4 )
   }
   '''  

   assert componenttools.is_well_formed_component(staff)
   assert staff.format == "\\new Staff {\n\tc'4\n\tg'4\n\tb8\n\tc'8\n\td'8 -\\staccato (\n\tef'8 ^\\marcato\n\t<bf cs' f'>4\n\tc'4 )\n}"
