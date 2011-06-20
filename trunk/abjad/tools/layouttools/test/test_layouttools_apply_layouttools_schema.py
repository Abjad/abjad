from abjad import *
import py
py.test.skip('skipping until clean way to pass multiline format contributions.')


def test_layouttools_apply_layouttools_schema_01( ):
   '''Short-cut to avoid instantiating SystemYOffsets,
   StaffAlignmentDistances, FixedStaffPositioning by hand.
   '''

   t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
   pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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
   ## then position the second staff 15 units below the first staff.

   schema = layouttools.LayoutSchema(Duration(4, 8), (40, 5, 1), (15, ))   
   layouttools.apply_layout_schema(t, schema)

   r'''
   \new Staff {
      {
         \overrideProperty #"Score.NonMusicalPaperColumn"
         #'line-break-system-details
         #'((Y-offset . 40) (alignment-distances . (15)))
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
         #'((Y-offset . 80) (alignment-distances . (15)))
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

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\new Staff {\n\t{\n\t\t\\overrideProperty #"Score.NonMusicalPaperColumn"\n\t\t#\'line-break-system-details\n\t\t#\'((Y-offset . 40) (alignment-distances . (15)))\n\t\t\\time 2/8\n\t\tc\'8\n\t\td\'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\te\'8\n\t\tf\'8\n\t\t\\break\n\t\t\\noPageBreak\n\t}\n\t{\n\t\t\\overrideProperty #"Score.NonMusicalPaperColumn"\n\t\t#\'line-break-system-details\n\t\t#\'((Y-offset . 80) (alignment-distances . (15)))\n\t\t\\time 2/8\n\t\tg\'8\n\t\ta\'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tb\'8\n\t\tc\'\'8\n\t\t\\break\n\t}\n}'


def test_layouttools_apply_layouttools_schema_02( ):
   '''Short-cut to avoid instantiating SystemYOffsets,
   StaffAlignmentDistances, FixedStaffPositioning by hand.

   Here operating on leaves instead of measures with optional klass keyword.
   '''

   t = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")

   r'''
   \new Staff {
      c'8
      d'8
      e'8
      f'8
      g'8
      a'8
      b'8
      c''8
   }
   '''

   schema = layouttools.LayoutSchema(Duration(4, 8), (40, 5, 1), (15, ))
   layouttools.apply_layout_schema(t, schema, klass = Note)

   r'''
   \new Staff {
      \overrideProperty #"Score.NonMusicalPaperColumn"
      #'line-break-system-details
      #'((Y-offset . 40) (alignment-distances . (15)))
      c'8
      d'8
      e'8
      f'8
      \break
      \noPageBreak
      \overrideProperty #"Score.NonMusicalPaperColumn"
      #'line-break-system-details
      #'((Y-offset . 80) (alignment-distances . (15)))
      g'8
      a'8
      b'8
      c''8
      \break
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\new Staff {\n\t\\overrideProperty #"Score.NonMusicalPaperColumn"\n\t#\'line-break-system-details\n\t#\'((Y-offset . 40) (alignment-distances . (15)))\n\tc\'8\n\td\'8\n\te\'8\n\tf\'8\n\t\\break\n\t\\noPageBreak\n\t\\overrideProperty #"Score.NonMusicalPaperColumn"\n\t#\'line-break-system-details\n\t#\'((Y-offset . 80) (alignment-distances . (15)))\n\tg\'8\n\ta\'8\n\tb\'8\n\tc\'\'8\n\t\\break\n}'
