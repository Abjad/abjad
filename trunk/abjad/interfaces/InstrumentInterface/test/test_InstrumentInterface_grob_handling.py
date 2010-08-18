from abjad import *


def test_InstrumentInterface_grob_handling_01( ):
   '''The Abjad InstrumentInterface handles the
   LilyPond InstrumentName grob.
   '''

   t = Staff(macros.scale(4))
   t.set.instrument_name = markuptools.Markup(r'\circle { V }')
   t.override.instrument_name.color = 'red'

   r'''
   \new Staff \with {
      \override InstrumentName #'color = #red
      instrumentName = \markup { \circle { V } }
   } {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff \\with {\n\t\\override InstrumentName #'color = #red\n\tinstrumentName = \\markup { \\circle { V } }\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
