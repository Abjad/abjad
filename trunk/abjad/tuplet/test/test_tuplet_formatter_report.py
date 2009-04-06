from abjad import *


def test_tuplet_formatter_report_01( ):
   '''Report format-time contributions.'''

   t = FixedDurationTuplet((2, 8), scale(3))
   t.accidental.style = 'forget'
   t.barline.type = '|.'
   t.clef.forced = 'treble'

   r'''\times 2/3 {
           #(set-accidental-style 'forget)
           \clef "treble"
           c'8
           d'8
           e'8
           \bar "|."
   }'''

   result = t.formatter.report('string')

   r'''<_TupletFormatter>
           opening
                   <_AccidentalInterface>
                           #(set-accidental-style 'forget)
                   <_ClefInterface>
                           \clef "treble"
           closing
                   <_BarLineInterface>
                           \bar "|."'''

   assert result == '<_TupletFormatter>\n\topening\n\t\t<_AccidentalInterface>\n\t\t\t#(set-accidental-style \'forget)\n\t\t<_ClefInterface>\n\t\t\t\\clef "treble"\n\tclosing\n\t\t<_BarLineInterface>\n\t\t\t\\bar "|."\n'
