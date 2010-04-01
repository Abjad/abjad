from abjad import *


def test_tonalharmony_mark_unlikely_melodic_intervals_in_chorale_01( ):
   
   ## c'4 is down an octave and should be c''4 instead
   note_entry_string = "b'4 d''2 c'4 b'4 a'2 g'2"
   soprano = lilytools.parse_note_entry_string(note_entry_string)
   tonalharmony.mark_unlikely_melodic_intervals_in_chorale(soprano, 'above')

   r'''
   {
           b'4
           \once \override Accidental #'color = #red
           \once \override Dots #'color = #red
           \once \override NoteHead #'color = #red
           \override Glissando #'color = #red
           \override Glissando #'thickness = #2
           d''2 \glissando
           \once \override Accidental #'color = #red
           \once \override Dots #'color = #red
           \once \override NoteHead #'color = #red
           \override Glissando #'color = #red
           \override Glissando #'thickness = #2
           c'4 ^ \markup { \with-color #red { -M9 } } \glissando
           \revert Glissando #'color
           \revert Glissando #'thickness
           \once \override Accidental #'color = #red
           \once \override Dots #'color = #red
           \once \override NoteHead #'color = #red
           b'4 ^ \markup { \with-color #red { +M7 } }
           \revert Glissando #'color
           \revert Glissando #'thickness
           a'2
           g'2
   }
   '''
   
   assert soprano.format == "{\n\tb'4\n\t\\once \\override Accidental #'color = #red\n\t\\once \\override Dots #'color = #red\n\t\\once \\override NoteHead #'color = #red\n\t\\override Glissando #'color = #red\n\t\\override Glissando #'thickness = #2\n\td''2 \\glissando\n\t\\once \\override Accidental #'color = #red\n\t\\once \\override Dots #'color = #red\n\t\\once \\override NoteHead #'color = #red\n\t\\override Glissando #'color = #red\n\t\\override Glissando #'thickness = #2\n\tc'4 ^ \\markup { \\with-color #red { -M9 } } \\glissando\n\t\\revert Glissando #'color\n\t\\revert Glissando #'thickness\n\t\\once \\override Accidental #'color = #red\n\t\\once \\override Dots #'color = #red\n\t\\once \\override NoteHead #'color = #red\n\tb'4 ^ \\markup { \\with-color #red { +M7 } }\n\t\\revert Glissando #'color\n\t\\revert Glissando #'thickness\n\ta'2\n\tg'2\n}"
