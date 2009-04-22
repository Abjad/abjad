from abjad import *


def test_partition_unfractured_by_counts_01( ):
   '''Partition container into parts of lengths equal to counts.
      Read list of counts only once; do not cycle.
      Fracture spanners attaching directly to container.
      Leave spanner attaching to container contents untouched.'''

   t = Voice([Container(construct.scale(8))])
   Beam(t[0])
   Slur(t[0].leaves)

   r'''\new Voice {
      {
         c'8 [ (
         d'8
         e'8
         f'8
         g'8
         a'8
         b'8
         c''8 ] )
      }
   }'''

   parts = partition.unfractured_by_counts(t[:], [1, 3])

   r'''\new Voice {
      {
         c'8 [ (
      }
      {
         d'8
         e'8
         f'8
      }
      {
         g'8
         a'8
         b'8
         c''8 ] )
      }
   }'''

   assert check.wf(t)
   assert len(parts) == 3
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t}\n\t{\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t\tb'8\n\t\tc''8 ] )\n\t}\n}"
