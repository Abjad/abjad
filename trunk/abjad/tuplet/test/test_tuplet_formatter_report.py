from abjad import *


def test_tuplet_formatter_report_01( ):
   '''Report format-time contributions.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3))
   t.accidental.style = 'forget'
   t.barline.kind = '|.'
   t.clef.forced = Clef('treble')

   r'''\times 2/3 {
           #(set-accidental-style 'forget)
           \clef "treble"
           c'8
           d'8
           e'8
           \bar "|."
   }'''

   result = t.formatter.report(output = 'string')

   r'''slot_1
   slot_2
      _BracketsInterface.open
         \times 2/3 {
   slot_3
      _InterfaceAggregator.opening
            #(set-accidental-style 'forget)
            \clef "treble"
   slot_4
      _TupletFormatter._contents
            c'8
            d'8
            e'8
   slot_5
      _InterfaceAggregator.closing
            \bar "|."
   slot_6
      _BracketsInterface.close
         }
   slot_7'''

   assert result == 'slot_1\nslot_2\n\t_BracketsInterface.open\n\t\t\\times 2/3 {\nslot_3\n\t_InterfaceAggregator.opening\n\t\t\t#(set-accidental-style \'forget)\n\t\t\t\\clef "treble"\nslot_4\n\t_TupletFormatter._contents\n\t\t\tc\'8\n\t\t\td\'8\n\t\t\te\'8\nslot_5\n\t_InterfaceAggregator.closing\n\t\t\t\\bar "|."\nslot_6\n\t_BracketsInterface.close\n\t\t}\nslot_7\n'
