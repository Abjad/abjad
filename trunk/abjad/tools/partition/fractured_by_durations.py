from abjad.tools.partition._by_durations import _by_durations


def fractured_by_durations(components, durations, tie_after = False):
   r'''Partition `components` by `durations`.
   Fracture all spanners attached to any component at
   any duration split-point.  ::

      abjad> t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2)
      abjad> pitchtools.diatonicize(t)
      abjad> Beam(t[0])
      abjad> Beam(t[1])
      abjad> Slur(t.leaves)
      abjad> f(t)
      \new Staff {
              {
                      \time 2/8
                      c'8 [ (
                      d'8 ]
              }
              {
                      \time 2/8
                      e'8 [
                      f'8 ] )
              }
      }

   ::

      abjad> durations = [Rational(1, 32), Rational(3, 32), Rational(5, 32)]
      abjad> parts = partition.fractured_by_durations(t[:1], durations)
      abjad> f(t)
      \new Staff {
              {
                      \time 1/32
                      c'32 [ ] ( )
              }
              {
                      \time 3/32
                      c'16. [ ] ( )
              }
              {
                      \time 4/32
                      d'8 [ ] (
              }
              {
                      \time 2/8
                      e'8 [
                      f'8 ] )
              }
      }
   '''

   return _by_durations(components, durations, 
      spanners = 'fractured', tie_after = tie_after)
