from abjad.tools.componenttools._partition_by_durations import _partition_by_durations


def split_components_once_by_prolated_durations_and_fracture_crossing_spanners(components, durations, tie_after = False):
   r'''Partition `components` by `durations`.
   Fracture all spanners attached to any component at
   any duration split-point.  ::

      abjad> t = Staff(RigidMeasure((2, 8), notetools.make_repeated_notes(2)) * 2)
      abjad> pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
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
      abjad> parts = componenttools.split_components_once_by_prolated_durations_and_fracture_crossing_spanners(t[:1], durations)
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

   .. versionchanged:: 1.1.2
      renamed ``partition.fractured_by_durations( )`` to
      ``componenttools.split_components_once_by_prolated_durations_and_fracture_crossing_spanners( )``.
   '''

   return _partition_by_durations(components, durations, 
      spanners = 'fractured', tie_after = tie_after)
