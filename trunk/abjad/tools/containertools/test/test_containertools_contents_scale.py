from abjad import *


def test_containertools_contents_scale_01( ):
   '''Scale leaves in voice by 3/2; ie, dot leaves.'''

   t = Voice(construct.scale(4))
   containertools.contents_scale(t, Rational(3, 2))

   r'''\new Voice {
           c'8.
           d'8.
           e'8.
           f'8.
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8.\n\td'8.\n\te'8.\n\tf'8.\n}"


def test_containertools_contents_scale_02( ):
   '''Scale leaves in voice by 5/4; ie, quarter-tie leaves.'''

   t = Voice(construct.scale(4))
   containertools.contents_scale(t, Rational(5, 4))

   r'''\new Voice {
           c'8 ~
           c'32
           d'8 ~
           d'32
           e'8 ~
           e'32
           f'8 ~
           f'32
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 ~\n\tc'32\n\td'8 ~\n\td'32\n\te'8 ~\n\te'32\n\tf'8 ~\n\tf'32\n}"


def test_containertools_contents_scale_03( ):
   '''Scale leaves in voice by untied nonbinary 4/3;
       ie, tupletize notes.'''

   t = Voice(construct.scale(4))
   containertools.contents_scale(t, Rational(4, 3))

   r'''\new Voice {
           \times 2/3 {
                   c'4
           }
           \times 2/3 {
                   d'4
           }
           \times 2/3 {
                   e'4
           }
           \times 2/3 {
                   f'4
           }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'4\n\t}\n\t\\times 2/3 {\n\t\td'4\n\t}\n\t\\times 2/3 {\n\t\te'4\n\t}\n\t\\times 2/3 {\n\t\tf'4\n\t}\n}"


def test_containertools_contents_scale_04( ):
   '''Scale leaves in voice by tied nonbinary 5/4;
       ie, tupletize notes.'''

   t = Voice(construct.scale(4))
   containertools.contents_scale(t, Rational(5, 6))

   r'''\new Voice {
           \times 2/3 {
                   c'8 ~
                   c'32
           }
           \times 2/3 {
                   d'8 ~
                   d'32
           }
           \times 2/3 {
                   e'8 ~
                   e'32
           }
           \times 2/3 {
                   f'8 ~
                   f'32
           }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 ~\n\t\tc'32\n\t}\n\t\\times 2/3 {\n\t\td'8 ~\n\t\td'32\n\t}\n\t\\times 2/3 {\n\t\te'8 ~\n\t\te'32\n\t}\n\t\\times 2/3 {\n\t\tf'8 ~\n\t\tf'32\n\t}\n}"


def test_containertools_contents_scale_05( ):
   '''Scale mixed notes and tuplets.'''

   t = Voice([Note(0, (3, 16)),
      FixedDurationTuplet((3, 8), construct.run(4))])
   pitchtools.diatonicize(t)

   r'''\new Voice {
      c'8.
      \fraction \times 3/4 {
         d'8
         e'8
         f'8
         g'8
      }
   }'''

   containertools.contents_scale(t, Rational(2, 3))

   r'''\new Voice {
      c'8
         d'16
         e'16
         f'16
         g'16
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8\n\t\td'16\n\t\te'16\n\t\tf'16\n\t\tg'16\n}"


def test_containertools_contents_scale_06( ):
   '''Undo scale of 5/4 with scale of 4/5.'''

   t = Voice(construct.scale(4))
   containertools.contents_scale(t, Rational(5, 4))

   r'''\new Voice {
      c'8 ~
      c'32
      d'8 ~
      d'32
      e'8 ~
      e'32
      f'8 ~
      f'32
   }'''
   assert t.format == "\\new Voice {\n\tc'8 ~\n\tc'32\n\td'8 ~\n\td'32\n\te'8 ~\n\te'32\n\tf'8 ~\n\tf'32\n}"

   containertools.contents_scale(t, Rational(4, 5))

   r'''\new Voice {
      c'8
      d'8
      e'8
      f'8
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_containertools_contents_scale_07( ):
   '''Double all contents, including measure.'''

   t = Voice(construct.run(2))
   t.append(RigidMeasure((2, 8), construct.run(2)))
   pitchtools.diatonicize(t)

   r'''\new Voice {
      c'8
      d'8
         \time 2/8
         e'8
         f'8
   }'''

   containertools.contents_scale(t, Rational(2))

   r'''\new Voice {
      c'4
      d'4
         \time 2/4
         e'4
         f'4
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'4\n\td'4\n\t\t\\time 2/4\n\t\te'4\n\t\tf'4\n}"


def test_containertools_contents_scale_08( ):
   '''Multiply all contents by 5/4, including measure.'''

   t = Voice(construct.run(2))
   t.append(RigidMeasure((2, 8), construct.run(2)))
   pitchtools.diatonicize(t)

   r'''\new Voice {
      c'8
      d'8
         \time 2/8
         e'8
         f'8
   }'''

   containertools.contents_scale(t, Rational(5, 4))

   r'''\new Voice {
      c'8 ~
      c'32
      d'8 ~
      d'32
         \time 20/64
         e'8 ~
         e'32
         f'8 ~
         f'32
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 ~\n\tc'32\n\td'8 ~\n\td'32\n\t\t\\time 20/64\n\t\te'8 ~\n\t\te'32\n\t\tf'8 ~\n\t\tf'32\n}"
