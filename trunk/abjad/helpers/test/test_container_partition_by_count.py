from abjad import *


def test_container_partition_by_count_01( ):
   '''Partition tuplet.'''

   t = FixedDurationTuplet((2, 8), scale(3))
   Beam(t[:])
   result = container_partition_by_count(t, [1, 2])

   r'''
   \times 2/3 {
      c'8 [
      d'8
      e'8 ]
   }
   '''

   assert check(t)
   assert t.format == "\\times 2/3 {\n\tc'8 [\n\td'8\n\te'8 ]\n}"

   r'''
   \times 2/3 {
      c'8 [ ]
   }
   '''

   assert check(result[0])
   assert result[0].format == "\\times 2/3 {\n\tc'8 [ ]\n}"

   r'''
   \times 2/3 {
      d'8 [
      e'8 ]
   }
   '''

   assert check(result[1])
   assert result[1].format == "\\times 2/3 {\n\td'8 [\n\te'8 ]\n}"


def test_container_partition_by_count_02( ):
   '''Partition voice.'''

   t = Voice(scale(3))
   Beam(t[:])
   result = container_partition_by_count(t, [1, 2])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8 ]
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8 ]\n}"

   r'''
   \new Voice {
      c'8 [ ]
   }
   '''

   assert check(result[0])
   assert result[0].format == "\\new Voice {\n\tc'8 [ ]\n}"

   r'''
   \new Voice {
      d'8 [
      e'8 ]
   }
   '''

   assert check(result[-1])
   assert result[-1].format == "\\new Voice {\n\td'8 [\n\te'8 ]\n}"
