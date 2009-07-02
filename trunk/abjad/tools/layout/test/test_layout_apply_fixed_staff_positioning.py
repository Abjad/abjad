from abjad import *


def test_layout_fixed_system_indicator_01( ):

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
   pitchtools.diatonicize(t)
   layout.line_break_every_prolated(t, Rational(4, 8))      

   r'''
   \new Staff {
           {
                   \time 2/8
                   c'8
                   d'8
           }
           {
                   \time 2/8
                   e'8
                   f'8
                   \break
           }
           {
                   \time 2/8
                   g'8
                   a'8
           }
           {
                   \time 2/8
                   b'8
                   c''8
                   \break
           }
   }
   '''

   systems = SystemYOffsets(20, 1)
   staves = StaffAlignmentOffsets(0)
   positioning = FixedStaffPositioning(systems, staves)
   layout.apply_fixed_staff_positioning(t, positioning)

   r'''
   \new Staff {
           {
                   \overrideProperty #"Score.NonMusicalPaperColumn"
                   #'line-break-system-details
                   #'((Y-offset . 0) (alignment-offsets . (0)))
                   \time 2/8
                   c'8
                   d'8
           }
           {
                   \time 2/8
                   e'8
                   f'8
                   \break
                   \pageBreak
           }
           {
                   \overrideProperty #"Score.NonMusicalPaperColumn"
                   #'line-break-system-details
                   #'((Y-offset . 0) (alignment-offsets . (0)))
                   \time 2/8
                   g'8
                   a'8
           }
           {
                   \time 2/8
                   b'8
                   c''8
                   \break
           }
   }
   '''

   assert check.wf(t)
   assert t.format == '\\new Staff {\n\t{\n\t\t\\overrideProperty #"Score.NonMusicalPaperColumn"\n\t\t#\'line-break-system-details\n\t\t#\'((Y-offset . 0) (alignment-offsets . (0)))\n\t\t\\time 2/8\n\t\tc\'8\n\t\td\'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\te\'8\n\t\tf\'8\n\t\t\\break\n\t\t\\pageBreak\n\t}\n\t{\n\t\t\\overrideProperty #"Score.NonMusicalPaperColumn"\n\t\t#\'line-break-system-details\n\t\t#\'((Y-offset . 0) (alignment-offsets . (0)))\n\t\t\\time 2/8\n\t\tg\'8\n\t\ta\'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tb\'8\n\t\tc\'\'8\n\t\t\\break\n\t}\n}'
