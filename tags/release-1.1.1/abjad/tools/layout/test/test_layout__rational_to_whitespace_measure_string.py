from abjad import *
from abjad.tools.layout._rational_to_whitespace_measure_string import \
   _rational_to_whitespace_measure_string as \
   layout__rational_to_whitespace_measure_string


def test_layout__rational_to_whitespace_measure_string_01( ):
   '''Turn nonbinary rational into whitespace measure string.'''

   t = layout__rational_to_whitespace_measure_string(Rational(1, 40))

   r'''
   {
           \override Staff.TimeSignature #'stencil = ##f
           \time 1/40
           \stopStaff
           \scaleDurations #'(4 . 5) {
                   s1 * 1/32
           }
           \startStaff
           \revert Staff.TimeSignature #'stencil
   }
   '''

   assert t == "{\n\t\\override Staff.TimeSignature #'stencil = ##f\n\t\\time 1/40\n\t\\stopStaff\n\t\\scaleDurations #'(4 . 5) {\n\t\ts1 * 1/32\n\t}\n\t\\startStaff\n\t\\revert Staff.TimeSignature #'stencil\n}"


def test_layout__rational_to_whitespace_measure_string_02( ):
   '''Turn binary rational into whitespace measure string.'''

   t = layout__rational_to_whitespace_measure_string(Rational(1, 32))

   r'''
   {
           \override Staff.TimeSignature #'stencil = ##f
           \time 1/32
           \stopStaff
           s1 * 1/32
           \startStaff
           \revert Staff.TimeSignature #'stencil
   }
   '''

   assert t == "{\n\t\\override Staff.TimeSignature #'stencil = ##f\n\t\\time 1/32\n\t\\stopStaff\n\ts1 * 1/32\n\t\\startStaff\n\t\\revert Staff.TimeSignature #'stencil\n}"
