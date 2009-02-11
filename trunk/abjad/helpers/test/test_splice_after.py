from abjad import *


def test_splice_after_01( ):
   '''Splice leaves after leaf.'''

   t = Voice(scale(3))
   Beam(t[:])
   result = splice_after(t[-1], scale(3))

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      c'8
      d'8
      e'8 ]
   }
   '''
   
   assert check(t)
   assert result == t[-4:]
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tc'8\n\td'8\n\te'8 ]\n}"


def test_splice_after_02( ):
   '''Splice tuplet after tuplet.'''

   t = Voice([FixedDurationTuplet((2, 8), scale(3))])
   Beam(t[0])
   result = splice_after(t[-1], [FixedDurationTuplet((2, 8), scale(3))])

   r'''
   \new Voice {
      \times 2/3 {
         c'8 [
         d'8
         e'8
      }
      \times 2/3 {
         c'8
         d'8
         e'8 ]
      }
   }
   '''

   assert check(t)
   assert result == t[:]
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8 ]\n\t}\n}"
