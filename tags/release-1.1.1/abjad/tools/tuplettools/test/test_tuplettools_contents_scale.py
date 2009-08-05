from abjad import *


def test_tuplettools_contents_scale_01( ):
   '''Double tuplet.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3))
   tuplettools.contents_scale(t, Rational(2))

   r'''\times 2/3 {
      c'4
      d'4
      e'4
   }'''

   assert check.wf(t)
   assert t.format == "\\times 2/3 {\n\tc'4\n\td'4\n\te'4\n}"


def test_tuplettools_contents_scale_02( ):
   '''Halve tuplet.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3))
   tuplettools.contents_scale(t, Rational(1, 2))

   r'''\times 2/3 {
      c'16
      d'16
      e'16
   }'''
   
   assert check.wf(t)
   assert t.format == "\\times 2/3 {\n\tc'16\n\td'16\n\te'16\n}"


def test_tuplettools_contents_scale_03( ):
   '''Quadruple tuplet.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3))
   tuplettools.contents_scale(t, Rational(4))

   r'''\times 2/3 {
      c'2
      d'2
      e'2
   }'''

   assert check.wf(t)
   assert t.format == "\\times 2/3 {\n\tc'2\n\td'2\n\te'2\n}"


def test_tuplettools_contents_scale_04( ):
   '''Quarter tuplet.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3))
   tuplettools.contents_scale(t, Rational(1, 4))

   r'''\times 2/3 {
      c'32
      d'32
      e'32
   }'''

   assert check.wf(t)
   assert t.format == "\\times 2/3 {\n\tc'32\n\td'32\n\te'32\n}"


def test_tuplettools_contents_scale_05( ):
   '''Multiply tuplet by 3/2.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3))
   tuplettools.contents_scale(t, Rational(3, 2))

   r'''c'8
      d'8
      e'8'''

   assert check.wf(t)
   assert t.format == "\tc'8\n\td'8\n\te'8"


def test_tuplettools_contents_scale_05( ):
   '''Multiply tuplet by 2/3.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3))
   tuplettools.contents_scale(t, Rational(2, 3))

   r'''\times 8/9 {
      c'16
      d'16
      e'16
   }'''

   assert check.wf(t)
   assert t.format == "\\times 8/9 {\n\tc'16\n\td'16\n\te'16\n}"


def test_tuplettools_contents_scale_06( ):
   '''Multiply tuplet by 3/5.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3))
   tuplettools.contents_scale(t, Rational(3, 5))

   r'''\times 4/5 {
      c'16
      d'16
      e'16
   }'''

   assert check.wf(t)
   assert t.format == "\\times 4/5 {\n\tc'16\n\td'16\n\te'16\n}"


def test_tuplettools_contents_scale_07( ):
   '''Multiply undotted, unbracketted notes by 3/2;
      ie, add a single dot.'''

   t = FixedDurationTuplet((3, 8), construct.scale(3))
   tuplettools.contents_scale(t, Rational(3, 2))

   r'''c'8.
      d'8.
      e'8.'''

   assert check.wf(t)
   assert t.format == "\tc'8.\n\td'8.\n\te'8."


def test_tuplettools_contents_scale_08( ):
   '''Binary target duration.'''

   t = FixedDurationTuplet((3, 8), [Note(0, (2, 8)), Note(0, (3, 8))])

   r'''\fraction \times 3/5 {
      c'4
      c'4.
   }'''

   tuplettools.contents_scale(t, Rational(2, 3))

   r'''\times 4/5 {
      c'8
      c'8.
   }'''

   assert check.wf(t)
   assert t.format == "\\times 4/5 {\n\tc'8\n\tc'8.\n}"


def test_tuplettools_contents_scale_09( ):
   '''Nonbinary target duration.'''

   t = FixedDurationTuplet((4, 8), [Note(0, (2, 8)), Note(0, (3, 8))])

   r'''\times 4/5 {
      c'4
      c'4.
   }'''

   tuplettools.contents_scale(t, Rational(2, 3))

   r'''\times 8/15 {
      c'4
      c'4.
   }'''
 
   assert check.wf(t)
   assert t.format == "\\times 8/15 {\n\tc'4\n\tc'4.\n}"
