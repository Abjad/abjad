from abjad import *


def test_tonalharmony_mark_unlikely_melodic_intervals_in_chorale_01( ):
   
   ## c'4 is down an octave and should be c''4 instead
   note_entry_string = "b'4 d''2 c'4 b'4 a'2 g'2"
   soprano = lilytools.parse_note_entry_string(note_entry_string)
   tonalharmony.mark_unlikely_melodic_intervals_in_chorale(soprano, 'above')

   r'''
   {
           b'4
           d''2
           \once \override NoteHead #'color = #red
           c'4 ^ \markup { \with-color #red { -M9 } }
           \once \override NoteHead #'color = #red
           b'4 ^ \markup { \with-color #red { +M7 } }
           a'2
           g'2
   }
   '''
   
   assert soprano.format == "{\n\tb'4\n\td''2\n\t\\once \\override NoteHead #'color = #red\n\tc'4 ^ \\markup { \\with-color #red { -M9 } }\n\t\\once \\override NoteHead #'color = #red\n\tb'4 ^ \\markup { \\with-color #red { +M7 } }\n\ta'2\n\tg'2\n}"
