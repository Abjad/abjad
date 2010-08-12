from abjad.tools.componenttools._partition_by_durations import _partition_by_durations


def split_components_cyclically_by_prolated_durations_and_fracture_crossing_spanners(components, durations, tie_after = False):
   r'''Partition `components` cyclically by `durations`
   and fracture spanners in the process::

      abjad> staff = Staff(RigidMeasure((2, 8), notetools.make_repeated_notes(2)) * 2)
      abjad> macros.diatonicize(staff)
      abjad> BeamSpanner(staff[0])
      abjad> BeamSpanner(staff[1])
      abjad> SlurSpanner(staff.leaves)
      abjad> f(staff)
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
      
      abjad> durations = [Rational(3, 32)]
      abjad> componenttools.split_components_cyclically_by_prolated_durations_and_fracture_crossing_spanners(staff.leaves, durations) 
      [[Note(c', 16.)], [Note(c', 32), Note(d', 16)], [Note(d', 16), Note(e', 32)], 
      [Note(e', 16.)], [Note(f', 16.)], [Note(f', 32)]]
      
   ::
      
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'16. ( ) [
            c'32 (
            d'16 )
            d'16 ] (
         }
         {
            \time 2/8
            e'32 ) [
            e'16. (
            f'16. )
            f'32 ] ( )
         }
      }

   Return list of partitioned components.

   .. versionchanged:: 1.1.2
      renamed ``partition.cyclic_fractured_by_durations( )`` to
      ``componenttools.split_components_cyclically_by_prolated_durations_and_fracture_crossing_spanners( )``.
   '''

   return _partition_by_durations(components, durations, 
      spanners = 'fractured', cyclic = True, tie_after = tie_after)
