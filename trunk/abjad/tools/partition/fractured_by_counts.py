from abjad.tools.partition._by_counts import _by_counts


def fractured_by_counts(components, counts):
   r'''Partition `components` into parts of lengths equal to `counts`.
   Read `counts` only once; do not cycle.
   Fracture spanners attaching directly to container.
   Leave spanners attaching to container contents untouched.
   Return Python list of partitioned parts. ::

      abjad> t = Voice([Container(leaftools.make_first_n_notes_in_ascending_diatonic_scale(8))])
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

      abjad> parts = partition.fractured_by_counts(t[:], [1, 3])
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
   '''

   return _by_counts(components, counts, spanners = 'fractured')
