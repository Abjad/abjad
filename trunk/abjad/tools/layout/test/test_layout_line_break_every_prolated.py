from abjad import *
from abjad.leaf.leaf import _Leaf


def test_layout_line_break_every_prolated_01( ):
   '''Iterate klasses in expr and accumulate prolated duration.
      Add line break after every total le line duration.'''

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

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t\t\\break\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tb'8\n\t\tc''8\n\t\t\\break\n\t}\n}"


def test_layout_line_break_every_prolated_02( ):
   '''Iterate klasses in expr and accumulate prolated duration.
      Add line break after every total le line duration.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
   pitchtools.diatonicize(t)
   layout.line_break_every_prolated(t, Rational(1, 8), klass = _Leaf)

   r'''
   \new Staff {
           {
                   \time 2/8
                   c'8
                   \break
                   d'8
                   \break
           }
           {
                   \time 2/8
                   e'8
                   \break
                   f'8
                   \break
           }
           {
                   \time 2/8
                   g'8
                   \break
                   a'8
                   \break
           }
           {
                   \time 2/8
                   b'8
                   \break
                   c''8
                   \break
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\t\\break\n\t\td'8\n\t\t\\break\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\t\\break\n\t\tf'8\n\t\t\\break\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\t\\break\n\t\ta'8\n\t\t\\break\n\t}\n\t{\n\t\t\\time 2/8\n\t\tb'8\n\t\t\\break\n\t\tc''8\n\t\t\\break\n\t}\n}"
