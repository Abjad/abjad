from abjad import *


def test_label_melodic_chromatic_intervals_01( ):

   staff = Staff(construct.scale(8))
   label.melodic_chromatic_intervals(staff)

   r'''
   \new Staff {
           c'8 ^ \markup { 1 }
           d'8 ^ \markup { 1 }
           e'8 ^ \markup { 1 }
           f'8 ^ \markup { 1 }
           g'8 ^ \markup { 1 }
           a'8 ^ \markup { 1 }
           b'8 ^ \markup { 1 }
           c''8
   }
   '''

   assert check.wf(staff)
   assert staff.format == "\\new Staff {\n\tc'8 ^ \\markup { 2 }\n\td'8 ^ \\markup { 2 }\n\te'8 ^ \\markup { 1 }\n\tf'8 ^ \\markup { 2 }\n\tg'8 ^ \\markup { 2 }\n\ta'8 ^ \\markup { 2 }\n\tb'8 ^ \\markup { 1 }\n\tc''8\n}"


def test_label_melodic_chromatic_intervals_02( ):

   staff = Staff(construct.notes([0, 13, 11, 8, 2, 3, 9, 10, 6, 5], [Rational(1, 8)]))
   label.melodic_chromatic_intervals(staff)

   r'''
   \new Staff {
           c'8 ^ \markup { 13 }
           cs''8 ^ \markup { -2 }
           b'8 ^ \markup { -2 }
           af'8 ^ \markup { -6 }
           d'8 ^ \markup { 1 }
           ef'8 ^ \markup { 6 }
           a'8 ^ \markup { 1 }
           bf'8 ^ \markup { -4 }
           fs'8 ^ \markup { -1 }
           f'8
   }
   '''

   assert check.wf(staff)
   assert staff.format == "\\new Staff {\n\tc'8 ^ \\markup { 13 }\n\tcs''8 ^ \\markup { -2 }\n\tb'8 ^ \\markup { -2 }\n\taf'8 ^ \\markup { -6 }\n\td'8 ^ \\markup { 1 }\n\tef'8 ^ \\markup { 6 }\n\ta'8 ^ \\markup { 1 }\n\tbf'8 ^ \\markup { -4 }\n\tfs'8 ^ \\markup { -1 }\n\tf'8\n}"
