from abjad import *
import py.test


py.test.skip('TODO: Make tuplet formatter report test work after formatter changes.')

def test_tuplet_formatter_report_01( ):
   '''Report format-time contributions.'''

   t = FixedDurationTuplet((2, 8), scale(3))
   t.accidental.style = 'forget'
   t.barline.type = '|.'
   t.clef.forced = 'treble'

   r'''<_TupletFormatter>
           _opening
                   <_AccidentalInterface>
                           #(set-accidental-style 'forget)
                   <_ClefInterface>
                           \clef "treble"
           _closing
                   <_BarLineInterface>
                           \bar "|."'''

   report = t.formatter.report('string') 
   assert report == '<_TupletFormatter>\n\t_opening\n\t\t<_AccidentalInterface>\n\t\t\t#(set-accidental-style \'forget)\n\t\t<_ClefInterface>\n\t\t\t\\clef "treble"\n\t_closing\n\t\t<_BarLineInterface>\n\t\t\t\\bar "|."\n'
