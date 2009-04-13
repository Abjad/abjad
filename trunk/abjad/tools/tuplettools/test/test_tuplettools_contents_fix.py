from abjad import *


def test_tuplettools_contents_fix_01( ):
   '''Halve note durations.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3, Rational(1, 4)))
   assert not durtools.is_tuplet_multiplier(t.duration.multiplier)

   r'''\times 1/3 {
      c'4
      d'4
      e'4
   }'''
   
   tuplettools.contents_fix(t)

   r'''\times 2/3 {
      c'8
      d'8
      e'8
   }'''

   assert check.wf(t)
   assert durtools.is_tuplet_multiplier(t.duration.multiplier)
   assert t.format == "\\times 2/3 {\n\tc'8\n\td'8\n\te'8\n}"


def test_tuplettools_contents_fix_02( ):
   '''Double note duration.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3, Rational(1, 32)))
   assert not durtools.is_tuplet_multiplier(t.duration.multiplier)

   r'''\times 8/3 {
      c'32
      d'32
      e'32
   }'''

   tuplettools.contents_fix(t)

   r'''\times 4/3 {
      c'16
      d'16
      e'16
   }'''

   assert check.wf(t)
   assert durtools.is_tuplet_multiplier(t.duration.multiplier)
   assert t.format == "\\times 4/3 {\n\tc'16\n\td'16\n\te'16\n}"


def test_tuplettools_contents_fix_03( ):
   '''Halve note durations.'''

   t = FixedDurationTuplet((5, 16), construct.scale(3, Rational(1, 4)))
   assert not durtools.is_tuplet_multiplier(t.duration.multiplier)

   r'''\fraction \times 5/12 {
      c'4
      d'4
      e'4
   }'''

   tuplettools.contents_fix(t)

   r'''\fraction \times 5/6 {
      c'8
      d'8
      e'8
   }'''

   assert check.wf(t)
   assert durtools.is_tuplet_multiplier(t.duration.multiplier)
   assert t.format == "\\fraction \\times 5/6 {\n\tc'8\n\td'8\n\te'8\n}"
