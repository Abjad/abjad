from abjad import *
import copy


def test_Voice___copy___01( ):
   '''Staves (shallow) copy grob overrides and context settings but not musical content.
   '''

   voice_1 = Voice("c'8 d'8 e'8 f'8")
   voice_1.override.note_head.color = 'red'
   voice_1.set.tuplet_full_length = True

      
   r'''
   \new Voice \with {
      \override NoteHead #'color = #red
      tupletFullLength = ##t
   } {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   voice_2 = copy.copy(voice_1)

   r'''
   \new Voice \with {
      \override NoteHead #'color = #red
      tupletFullLength = ##t
   } {
   }
   '''

   assert voice_2.format == "\\new Voice \\with {\n\t\\override NoteHead #'color = #red\n\ttupletFullLength = ##t\n} {\n}"
