from abjad import *


def test_clonewp_by_leaf_counts_with_parentage_01( ):
   '''Partition tuplet in voice.
      The helper wraps lcopy( ).
      This means that the original structure remains unchanged.
      Also that resulting parts cut all the way up into voice.'''

   t = Voice([FixedDurationTuplet((2, 8), construct.scale(3))])
   Beam(t[0][:])
   left, right = clonewp.by_leaf_counts_with_parentage(t[0], [1, 2])

   r'''\new Voice {
           \times 2/3 {
                   c'8 [ ]
           }
   }'''

   assert check.wf(left)
   assert left.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [ ]\n\t}\n}"

   r'''\new Voice {
           \times 2/3 {
                   d'8 [
                   e'8 ]
           }
   }'''

   assert check.wf(t)
   assert right.format == "\\new Voice {\n\t\\times 2/3 {\n\t\td'8 [\n\t\te'8 ]\n\t}\n}"


def test_clonewp_by_leaf_counts_with_parentage_02( ):
   '''Partition voice.'''

   t = Voice(construct.scale(3))
   Beam(t[:])
   result = clonewp.by_leaf_counts_with_parentage(t, [1, 2])

   r'''\new Voice {
      c'8 [
      d'8
      e'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8 ]\n}"

   r'''\new Voice {
      c'8 [ ]
   }'''

   assert check.wf(result[0])
   assert result[0].format == "\\new Voice {\n\tc'8 [ ]\n}"

   r'''\new Voice {
      d'8 [
      e'8 ]
   }'''

   assert check.wf(result[-1])
   assert result[-1].format == "\\new Voice {\n\td'8 [\n\te'8 ]\n}"
