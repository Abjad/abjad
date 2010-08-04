from abjad.tools.componenttools._partition_by_counts import _partition_by_counts


def partition_components_once_by_counts_and_fracture_crossing_spanners(components, counts):
   r'''Partition `components` into parts of lengths equal to `counts`.
   Read `counts` only once; do not cycle.
   Fracture spanners attaching directly to container.
   Leave spanners attaching to container contents untouched.
   Return Python list of partitioned parts. ::

      abjad> t = Voice([Container(macros.scale(8))])
      abjad> Beam(t[0])
      abjad> Slur(t[0].leaves)
      abjad> f(t)
      \new Voice {
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
      }

   ::

      abjad> parts = componenttools.partition_components_once_by_counts_and_fracture_crossing_spanners(t[:], [1, 3])
      abjad> f(t)
      \new Voice {
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
      }

   .. versionchanged:: 1.1.2
      renamed ``partition.fractured_by_counts( )`` to
      ``componenttools.partition_components_once_by_counts_and_fracture_crossing_spanners( )``.
   '''

   return _partition_by_counts(components, counts, spanners = 'fractured')
