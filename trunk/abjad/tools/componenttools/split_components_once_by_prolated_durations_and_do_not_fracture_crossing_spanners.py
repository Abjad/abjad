from abjad.tools.componenttools._partition_by_durations import _partition_by_durations


def split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners(components, durations, tie_after = False):
   r'''Partition `components` according to `durations`.
   Do not fracture spanners. ::

      abjad> t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
      abjad> macros.diatonicize(t)
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
      abjad> parts = componenttools.split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners(t[:1], durations)
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

   .. versionchanged:: 1.1.2
      renamed ``partition.unfractured_by_durations( )`` to
      ``componenttools.split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners( )``.
   '''

   return _partition_by_durations(components, durations, 
      spanners = 'unfractured', tie_after = tie_after)
