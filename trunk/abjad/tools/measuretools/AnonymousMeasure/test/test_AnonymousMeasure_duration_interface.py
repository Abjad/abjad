from abjad import *


def test_AnonymousMeasure_duration_interface_01( ):
   '''Notes as contents.'''

   t = measuretools.AnonymousMeasure(macros.scale(4))

   r'''
   {
           \override Staff.TimeSignature #'stencil = ##f
           \time 1/2
           c'8
           d'8
           e'8
           f'8
           \revert Staff.TimeSignature #'stencil
   }
   '''

   assert t.duration.contents == Rational(4, 8)
   assert t.duration.preprolated == Rational(4, 8)
   assert t.duration.prolated == Rational(4, 8)
   assert t.duration.prolation == 1

   assert t.format == "{\n\t\\override Staff.TimeSignature #'stencil = ##f\n\t\\time 1/2\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert Staff.TimeSignature #'stencil\n}"


def test_AnonymousMeasure_duration_interface_02( ):
   '''Works with binary tuplet as contents.'''

   t = measuretools.AnonymousMeasure([tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))])

   r'''
   {
           \override Staff.TimeSignature #'stencil = ##f
           \time 1/4
           \times 2/3 {
                   c'8
                   d'8
                   e'8
           }
           \revert Staff.TimeSignature #'stencil
   }
   '''

   assert t.duration.contents == Rational(2, 8)
   assert t.duration.preprolated == Rational(2, 8)
   assert t.duration.prolated == Rational(2, 8)
   assert t.duration.prolation == 1

   #assert t.format == "{\n\t\\override Staff.TimeSignature #'stencil = ##f\n\t\\time 1/4\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n\t\\revert Staff.TimeSignature #'stencil\n}"
   assert t.format == "{\n\t\\override Staff.TimeSignature #'stencil = ##f\n\t\\times 2/3 {\n\t\t\\time 1/4\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n\t\\revert Staff.TimeSignature #'stencil\n}"


def test_AnonymousMeasure_duration_interface_03( ):
   '''Works with nonbinary tuplet.'''

   t = measuretools.AnonymousMeasure([Tuplet((2, 3), macros.scale(4))])
   t.denominator = 12

   r'''
   {
           \override Staff.TimeSignature #'stencil = ##f
           \time 4/12
           \times 2/3 {
                   c'8
                   d'8
                   e'8
                   f'8
           }
           \revert Staff.TimeSignature #'stencil
   }
   '''

   assert t.duration.contents == Rational(4, 12)
   assert t.duration.preprolated == Rational(4, 12)
   assert t.duration.prolated == Rational(4, 12)
   assert t.duration.prolation == 1

   #assert t.format == "{\n\t\\override Staff.TimeSignature #'stencil = ##f\n\t\\time 4/12\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n\t\\revert Staff.TimeSignature #'stencil\n}"
   assert t.format == "{\n\t\\override Staff.TimeSignature #'stencil = ##f\n\t\\times 2/3 {\n\t\t\\time 4/12\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n\t\\revert Staff.TimeSignature #'stencil\n}"
