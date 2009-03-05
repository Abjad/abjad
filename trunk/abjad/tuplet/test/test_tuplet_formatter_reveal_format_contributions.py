from abjad import *


def test_tuplet_formatter_reveal_format_locations_01( ):
   t = FixedDurationTuplet((2, 8), scale(3))
   t.accidental.style = 'forget'
   t.barline.type = 'final'
   t.clef.forced = 'treble'

   r'''
   _before
      <_AccidentalInterface>
         #(set-accidental-style 'forget)
      <_ClefInterface>
         \clef treble
   _opening
      <_AccidentalInterface>
         #(set-accidental-style 'forget)
      <_ClefInterface>
         \clef treble
   _closing
      <_BarLineInterface>
         \bar "|."
   '''

   assert t.formatter._revealFormatContributions( ) == '_before\n\t<_AccidentalInterface>\n\t\t#(set-accidental-style \'forget)\n\t<_ClefInterface>\n\t\t\\clef treble\n_opening\n\t<_AccidentalInterface>\n\t\t#(set-accidental-style \'forget)\n\t<_ClefInterface>\n\t\t\\clef treble\n_closing\n\t<_BarLineInterface>\n\t\t\\bar "|."\n'
