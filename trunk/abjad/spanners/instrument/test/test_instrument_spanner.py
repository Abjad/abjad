from abjad import *


def test_instrument_spanner_01( ):
   '''Instrument spanner with long and short names.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   p = Instrument(t, 'Alto Flute in G', 'Fl. G')

   r'''
   \new Voice {
      \set Staff.instrumentName = \markup { Alto Flute in G }
      \set Staff.shortInstrumentName = \markup { Fl. G }
      c'8
      d'8
      e'8
      f'8
      \unset Staff.instrumentName
      \unset Staff.shortInstrumentName
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\\set Staff.instrumentName = \\markup { Alto Flute in G }\n\t\\set Staff.shortInstrumentName = \\markup { Fl. G }\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\unset Staff.instrumentName\n\t\\unset Staff.shortInstrumentName\n}"


def test_instrument_spanner_02( ):
   '''Works with markup.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   long_name = Markup(r'\italic { Alto Flute in G }')
   short_name = Markup(r'\italic { Fl. G }')
   p = Instrument(t, long_name, short_name)

   r'''
   \new Voice {
      \set Staff.instrumentName = \markup { \italic { Alto Flute in G } }
      \set Staff.shortInstrumentName = \markup { \italic { Fl. G } }
      c'8
      d'8
      e'8
      f'8
      \unset Staff.instrumentName
      \unset Staff.shortInstrumentName
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\\set Staff.instrumentName = \\markup { \\italic { Alto Flute in G } }\n\t\\set Staff.shortInstrumentName = \\markup { \\italic { Fl. G } }\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\unset Staff.instrumentName\n\t\\unset Staff.shortInstrumentName\n}"
