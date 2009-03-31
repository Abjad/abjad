from abjad import *


def test_instrument_spanner_01( ):
   '''Instrument spanner with long and short names.'''

   t = Voice(scale(4))
   p = Instrument(t, 'Alto Flute in G', 'Fl. G')

   r'''\new Voice {
      \set Staff.instrumentName = Alto Flute in G
      \set Staff.shortInstrumentName = Fl. G
      c'8
      d'8
      e'8
      f'8
      \unset Staff.instrumentName
      \unset Staff.shortInstrumentName
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\\set Staff.instrumentName = Alto Flute in G\n\t\\set Staff.shortInstrumentName = Fl. G\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\unset Staff.instrumentName\n\t\\unset Staff.shortInstrumentName\n}"
