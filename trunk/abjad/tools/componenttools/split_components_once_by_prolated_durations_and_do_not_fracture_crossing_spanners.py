from abjad.tools.componenttools._split_components_by_prolated_durations import _split_components_by_prolated_durations


def split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners(
   components, durations, tie_after = False):
   r'''.. versionadded:: 1.1.1

   Partition `components` according to `durations`.
   Do not fracture spanners. ::

      abjad> t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
      abjad> macros.diatonicize(t)
      abjad> spannertools.BeamSpanner(t[0])
      abjad> spannertools.BeamSpanner(t[1])
      abjad> spannertools.SlurSpanner(t.leaves)
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

      abjad> durations = [Fraction(1, 32), Fraction(3, 32), Fraction(5, 32)]
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

   return _split_components_by_prolated_durations(components, durations, 
      spanners = 'unfractured', tie_after = tie_after)
