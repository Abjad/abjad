from abjad import *


def test_label_melodic_counterpoint_intervals_01( ):

   staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(8))
   label.melodic_counterpoint_intervals(staff)

   r'''
      \new Staff {
              c'8 ^ \markup { +2 }
              d'8 ^ \markup { +2 }
              e'8 ^ \markup { +2 }
              f'8 ^ \markup { +2 }
              g'8 ^ \markup { +2 }
              a'8 ^ \markup { +2 }
              b'8 ^ \markup { +2 }
              c''8
      }
   '''

   assert check.wf(staff)
   assert staff.format == "\\new Staff {\n\tc'8 ^ \\markup { +2 }\n\td'8 ^ \\markup { +2 }\n\te'8 ^ \\markup { +2 }\n\tf'8 ^ \\markup { +2 }\n\tg'8 ^ \\markup { +2 }\n\ta'8 ^ \\markup { +2 }\n\tb'8 ^ \\markup { +2 }\n\tc''8\n}"


def test_label_melodic_counterpoint_intervals_02( ):

   staff = Staff(leaftools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Rational(1, 8)]))
   label.melodic_counterpoint_intervals(staff)

   r"""
   \new Staff {
           c'8 ^ \markup { +15 }
           cs'''8 ^ \markup { -9 }
           b'8 ^ \markup { -9 }
           af8 ^ \markup { -7 }
           bf,8 ^ \markup { 1 }
           b,8 ^ \markup { +14 }
           a'8 ^ \markup { +2 }
           bf'8 ^ \markup { -4 }
           fs'8 ^ \markup { 1 }
           f'8
   }
   """

   assert check.wf(staff)
   assert staff.format == "\\new Staff {\n\tc'8 ^ \\markup { +15 }\n\tcs'''8 ^ \\markup { -9 }\n\tb'8 ^ \\markup { -9 }\n\taf8 ^ \\markup { -7 }\n\tbf,8 ^ \\markup { 1 }\n\tb,8 ^ \\markup { +14 }\n\ta'8 ^ \\markup { +2 }\n\tbf'8 ^ \\markup { -4 }\n\tfs'8 ^ \\markup { 1 }\n\tf'8\n}"
