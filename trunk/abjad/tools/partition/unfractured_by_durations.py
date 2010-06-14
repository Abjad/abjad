from abjad.tools.partition._by_durations import _by_durations


def unfractured_by_durations(components, durations, tie_after = False):
   r'''Partition `components` according to `durations`.
   Do not fracture spanners. ::

      abjad> t = Staff(Container(leaftools.make_repeated_notes(2)) * 2)
      abjad> pitchtools.diatonicize(t)
      abjad> Beam(t[0])
      abjad> Beam(t[1])
      abjad> Slur(t.leaves)
      abjad> f(t)
      \new Staff {
         {
            c'8 [ (
            d'8 ]
         }
         {
            e'8 [
            f'8 ] )
         }
      }

   ::

      abjad> durations = [Rational(1, 32), Rational(3, 32), Rational(5, 32)]
      abjad> parts = partition.unfractured_by_durations(t[:1], durations)
      \new Staff {
         {
            c'32 [ (
         }
         {
            c'16.
         }
         {
            d'8 ]
         }
         {
            e'8 [
            f'8 ] )
         }
      }
   '''

   return _by_durations(components, durations, 
      spanners = 'unfractured', tie_after = tie_after)
