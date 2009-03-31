from abjad import *


def test_tuplet_formatter_reveal_format_contributions_01( ):
   t = FixedDurationTuplet((2, 8), scale(3))
   t.accidental.style = 'forget'
   t.barline.type = '|.'
   t.clef.forced = 'treble'

   r'''_opening
      <_AccidentalInterface>
         #(set-accidental-style 'forget)
      <_ClefInterface>
         \clef "treble"
   _closing
      <_BarLineInterface>
         \bar "|."'''

   assert t.formatter._revealFormatContributions( ) == '_opening\n\t<_AccidentalInterface>\n\t\t#(set-accidental-style \'forget)\n\t<_ClefInterface>\n\t\t\\clef "treble"\n_closing\n\t<_BarLineInterface>\n\t\t\\bar "|."\n'
