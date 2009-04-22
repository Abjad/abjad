from abjad import *


def test_partition_fractured_by_counts_01( ):
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

   parts = partition.fractured_by_counts(t[:], [1, 3])

   r'''\new Voice {
      {
         c'8 [ ] (
      }
      {
         d'8 [
         e'8
         f'8 ]
      }
      {
         g'8 [
         a'8
         b'8
         c''8 ] )
      }
   }'''

   assert check.wf(t)
   assert len(parts) == 3
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ ] (\n\t}\n\t{\n\t\td'8 [\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8\n\t\tb'8\n\t\tc''8 ] )\n\t}\n}"


def test_partition_fractured_by_counts_02( ):
   '''Partition by large part count.
      Input container cedes contents to new instance.
      Expression appears unaltered.'''

   t = Voice([Container(construct.scale(4))])
   Beam(t[0])
   Slur(t[0].leaves)
   container = t[0]

   r'''\new Voice {
           {
                   c'8 [ (
                   d'8
                   e'8
                   f'8 ] )
           }
   }'''

   parts = partition.fractured_by_counts(t[:], [100])

   r'''\new Voice {
           {
                   c'8 [ (
                   d'8
                   e'8
                   f'8 ] )
           }
   }'''

   assert check.wf(t)
   assert len(parts) == 1
   assert container is not t[0]
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t\td'8\n\t\te'8\n\t\tf'8 ] )\n\t}\n}"


def test_partition_fractured_by_counts_03( ):
   '''Partition by large number of part counts.
      First part counts apply and extra part counts do not apply.
      Result contains no empty parts.'''

   t = Voice([Container(construct.scale(4))])
   Beam(t[0])
   Slur(t[0].leaves)

   r'''\new Voice {
           {
                   c'8 [ (
                   d'8
                   e'8
                   f'8 ] )
           }
   }'''

   parts = partition.fractured_by_counts(t[:], [2, 2, 2, 2, 2])

   r'''\new Voice {
           {
                   c'8 [ (
                   d'8 ]
           }
           {
                   e'8 [
                   f'8 ] )
           }
   }'''

   assert check.wf(t)
   assert len(parts) == 2
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_partition_fractured_by_counts_04( ):
   '''Partition by empty part counts list.
      Input container returns within one-element result list.'''

   t = Voice([Container(construct.scale(4))])
   Beam(t[0])
   Slur(t[0].leaves)

   r'''\new Voice {
           {
                   c'8 [ (
                   d'8
                   e'8
                   f'8 ] )
           }
   }'''

   parts = partition.fractured_by_counts(t[:], [ ])

   r'''\new Voice {
           {
                   c'8 [ (
                   d'8
                   e'8
                   f'8 ] )
           }
   }'''

   assert check.wf(t)
   assert len(parts) == 1
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t\td'8\n\t\te'8\n\t\tf'8 ] )\n\t}\n}"
