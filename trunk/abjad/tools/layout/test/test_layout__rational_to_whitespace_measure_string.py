from abjad import *
from abjad.tools.layout._rational_to_whitespace_measure_string import \
   _rational_to_whitespace_measure_string as \
   layout__rational_to_whitespace_measure_string

import py.test
py.test.skip('measure redo')


def test_layout__rational_to_whitespace_measure_string_01( ):
   '''Turn rational into whitespace measure string.'''

   t = layout__rational_to_whitespace_measure_string(Rational(1, 32))

   r'''\override Staff.TimeSignature #'stencil = ##f
     \time 1/32
     \stopStaff
     s1 * 1/32
     \startStaff
     \revert Staff.TimeSignature #'stencil'''

   assert t == "\t\\override Staff.TimeSignature #'stencil = ##f\n\t\\time 1/32\n\t\\stopStaff\n\ts1 * 1/32\n\t\\startStaff\n\t\\revert Staff.TimeSignature #'stencil"
