from abjad import *


def test_layout_apply_layout_schema_01( ):
   '''Short-cut to avoid instantiating SystemYOffsets,
   StaffAlignmentOffsets, FixedStaffPositioning by hand.
   '''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
   pitchtools.diatonicize(t)

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
           }
   }
   '''

   ## what this says is line break after every 4/8 prolated duration;
   ## then position 5 systems per page;
   ## then space systems 40 units apart vertically;
   ## then leave blank space equivalent to 1 system at top of first page;
   ## then offset the two staves in each system at 0 and -15 vertical units.

   schema = layout.LayoutSchema(Rational(4, 8), (40, 5, 1), (0, -15))   
   layout.apply_layout_schema(t, schema)

   r'''
   \new Staff {
           {
                   \overrideProperty #"Score.NonMusicalPaperColumn"
                   #'line-break-system-details
                   #'((Y-offset . 40) (alignment-offsets . (0 -15)))
                   \time 2/8
                   c'8
                   d'8
           }
           {
                   \time 2/8
                   e'8
                   f'8
                   \break
                   \noPageBreak
           }
           {
                   \overrideProperty #"Score.NonMusicalPaperColumn"
                   #'line-break-system-details
                   #'((Y-offset . 80) (alignment-offsets . (0 -15)))
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
   assert t.format == '\\new Staff {\n\t{\n\t\t\\overrideProperty #"Score.NonMusicalPaperColumn"\n\t\t#\'line-break-system-details\n\t\t#\'((Y-offset . 40) (alignment-offsets . (0 -15)))\n\t\t\\time 2/8\n\t\tc\'8\n\t\td\'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\te\'8\n\t\tf\'8\n\t\t\\break\n\t\t\\noPageBreak\n\t}\n\t{\n\t\t\\overrideProperty #"Score.NonMusicalPaperColumn"\n\t\t#\'line-break-system-details\n\t\t#\'((Y-offset . 80) (alignment-offsets . (0 -15)))\n\t\t\\time 2/8\n\t\tg\'8\n\t\ta\'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tb\'8\n\t\tc\'\'8\n\t\t\\break\n\t}\n}'
