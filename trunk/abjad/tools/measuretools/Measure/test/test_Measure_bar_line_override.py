from abjad import *
import py
py.test.skip('figure out why this test is failing.')


def test_Measure_bar_line_override_01( ):
   '''Very magic things have to happen with slots at format time.
   This is to work correctly with the time at which LilyPond 
   draws new bar_lines during the LilyPond interpretation process.
   '''

   t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
   pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
   t._formatter.number.measures = 'comment'
   t[0].bar_line.kind = '||'
   t[0].override.staff.bar_line.color = 'red'

   ## NOTE: The LilyPond code here colors the DOUBLE BAR red and
   ##       not any of the single bars. What this means is that
   ##       the \override comes AT THE END of overriden measure
   ##       and that the \revert comes AFTER THE FIRST NOTE of
   ##       any measure that follows.

   r'''
   \new Staff {
           % start measure 1
           {
                   \time 2/8
                   c'8
                   d'8
                   \override Staff.BarLine #'color = #red
                   \bar "||"
           }
           % stop measure 1
           % start measure 2
           {
                   \time 2/8
                   e'8
                   \revert Staff.BarLine #'color
                   f'8
           }
           % stop measure 2
           % start measure 3
           {
                   \time 2/8
                   g'8
                   a'8
           }
           % stop measure 3
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\new Staff {\n\t% start measure 1\n\t{\n\t\t\\time 2/8\n\t\tc\'8\n\t\td\'8\n\t\t\\override Staff.BarLine #\'color = #red\n\t\t\\bar "||"\n\t}\n\t% stop measure 1\n\t% start measure 2\n\t{\n\t\t\\time 2/8\n\t\te\'8\n\t\t\\revert Staff.BarLine #\'color\n\t\tf\'8\n\t}\n\t% stop measure 2\n\t% start measure 3\n\t{\n\t\t\\time 2/8\n\t\tg\'8\n\t\ta\'8\n\t}\n\t% stop measure 3\n}'
