from abjad import *


def test_TupletNumberInterface_grob_handling_01( ):
   '''Abjad tuplets wrap grob overrides at before and after.'''

   t = FixedDurationTuplet((2, 8), macros.scale(3))
   #t.tuplet_number.fraction = True
   t.override.tuplet_number.fraction = True

   r'''
   \override TupletNumber #'fraction = ##t
   \times 2/3 {
           c'8
           d'8
           e'8
   }
   \revert TupletNumber #'fraction
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\override TupletNumber #'fraction = ##t\n\\times 2/3 {\n\tc'8\n\td'8\n\te'8\n}\n\\revert TupletNumber #'fraction"


def test_TupletNumberInterface_grob_handling_02( ):
   '''Override LilyPond TupletNumber grob on Abjad voice.'''

   t = Voice(macros.scale(4))
   spannertools.BeamSpanner(t[:])
   #t.tuplet_number.fraction = True
   t.override.tuplet_number.fraction = True

   r'''
   \new Voice \with {
           \override TupletNumber #'fraction = ##t
   } {
           c'8 [
           d'8
           e'8
           f'8 ]
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice \\with {\n\t\\override TupletNumber #'fraction = ##t\n} {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"

def test_TupletNumberInterface_grob_handling_03( ):
   '''Override LilyPond TupletNumber grob on Abjad leaf.'''

   t = Voice(macros.scale(4))
   spannertools.BeamSpanner(t[:])
   #t[1].tuplet_number.fraction = True
   t[1].override.tuplet_number.fraction = True

   r'''
   \new Voice {
           c'8 [
           \once \override TupletNumber #'fraction = ##t
           d'8
           e'8
           f'8 ]
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\t\\once \\override TupletNumber #'fraction = ##t\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_TupletNumberInterface_grob_handling_04( ):
   '''Override LilyPond TupletNumber text attribute.'''

   t = Voice(macros.scale(4))
   spannertools.BeamSpanner(t[:])
   #t.tuplet_number.text = Markup('"6:4"')
   t.override.tuplet_number.text = Markup('"6:4"')

   r'''
   \new Voice \with {
           \override TupletNumber #'text = \markup { "6:4" }
   } {
           c'8 [
           d'8
           e'8
           f'8 ]
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\new Voice \\with {\n\t\\override TupletNumber #\'text = \\markup { "6:4" }\n} {\n\tc\'8 [\n\td\'8\n\te\'8\n\tf\'8 ]\n}'
