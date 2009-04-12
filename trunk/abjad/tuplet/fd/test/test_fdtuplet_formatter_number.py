from abjad import *


def test_fdtuplet_formatter_number_01( ):
   '''Tuplet formatter number interface can contribute
      markup to many notes at format-time at once.'''

   t = FixedDurationTuplet((4, 8), scale(5))
   t.formatter.number.leaves = 'markup'

   r'''
   \times 4/5 {
           c'8 ^ \markup { 0 }
           d'8 ^ \markup { 1 }
           e'8 ^ \markup { 2 }
           f'8 ^ \markup { 3 }
           g'8 ^ \markup { 4 }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\times 4/5 {\n\tc'8 ^ \\markup { 0 }\n\td'8 ^ \\markup { 1 }\n\te'8 ^ \\markup { 2 }\n\tf'8 ^ \\markup { 3 }\n\tg'8 ^ \\markup { 4 }\n}"


def test_fdtuplet_formatter_number_02( ):
   '''Tuplet formatter number interface can contribute
      LilyPond comments to many notes at format-time at once.'''

   t = FixedDurationTuplet((4, 8), scale(5))
   t.formatter.number.leaves = 'comment'

   r'''
   \times 4/5 {
           c'8 % leaf 0
           d'8 % leaf 1
           e'8 % leaf 2
           f'8 % leaf 3
           g'8 % leaf 4
   }
   '''

   assert check.wf(t)
   assert t.format == "\\times 4/5 {\n\tc'8 % leaf 0\n\td'8 % leaf 1\n\te'8 % leaf 2\n\tf'8 % leaf 3\n\tg'8 % leaf 4\n}"
