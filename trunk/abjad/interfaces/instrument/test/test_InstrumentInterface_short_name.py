from abjad import *


def test_InstrumentInterface_short_name_01( ):
   '''Instrument interface short_name manages the LilyPond
   shortInstrumentName context setting.
   Works with strings.
   '''

   t = Staff(macros.scale(4))
   t.instrument.short_name = 'Vni. I'

   r'''
   \new Staff \with {
      shortInstrumentName = "Vni. I"
   } {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\new Staff \\with {\n\tshortInstrumentName = "Vni. I"\n} {\n\tc\'8\n\td\'8\n\te\'8\n\tf\'8\n}'


def test_InstrumentInterface_short_name_02( ):
   '''Works with Markup.'''

   t = Staff(macros.scale(4))
   t.instrument.short_name = Markup(r'\circle { V }')

   r'''
   \new Staff \with {
      shortInstrumentName = \markup { \circle { V } }
   } {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff \\with {\n\tshortInstrumentName = \\markup { \\circle { V } }\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
