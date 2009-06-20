from abjad import *


def test_layout_insert_measure_padding_01( ):

   t = Staff(AnonymousMeasure(construct.scale(2)) * 2)

   r'''\new Staff {
                   \override Staff.TimeSignature #'stencil = ##f
                   \time 1/4
                   c'8
                   d'8
                   \revert Staff.TimeSignature #'stencil
                   \override Staff.TimeSignature #'stencil = ##f
                   \time 1/4
                   c'8
                   d'8
                   \revert Staff.TimeSignature #'stencil
   }'''
   
   layout.insert_measure_padding(t, Rational(1, 32), Rational(1, 64))   

   r'''\new Staff {
                   \override Staff.TimeSignature #'stencil = ##f
                   \time 19/64
                   r32
                   c'8
                   d'8
                   r64
                   \revert Staff.TimeSignature #'stencil
                   \override Staff.TimeSignature #'stencil = ##f
                   \time 19/64
                   r32
                   c'8
                   d'8
                   r64
                   \revert Staff.TimeSignature #'stencil
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\t\\override Staff.TimeSignature #'stencil = ##f\n\t\t\\time 19/64\n\t\tr32\n\t\tc'8\n\t\td'8\n\t\tr64\n\t\t\\revert Staff.TimeSignature #'stencil\n\t\t\\override Staff.TimeSignature #'stencil = ##f\n\t\t\\time 19/64\n\t\tr32\n\t\tc'8\n\t\td'8\n\t\tr64\n\t\t\\revert Staff.TimeSignature #'stencil\n}"
