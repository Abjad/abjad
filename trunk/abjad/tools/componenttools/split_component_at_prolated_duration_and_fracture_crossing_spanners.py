from abjad.tools.componenttools._split_component_at_duration import _split_component_at_duration


def split_component_at_prolated_duration_and_fracture_crossing_spanners(
   component, prolated_duration, tie_after = False):
   r'''.. versionadded:: 1.1.1

   Split `component` at `prolated_duration` and fracture crossing spanners.

   Return split parts::

      abjad> t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
      abjad> macros.diatonicize(t)
      abjad> spannertools.BeamSpanner(t[0])
      abjad> spannertools.BeamSpanner(t[1])
      abjad> spannertools.SlurSpanner(t.leaves)
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

      halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t.leaves[0], Fraction(1, 32))
      \new Staff {
         {
            \time 2/8
            c'32 ( ) [
            c'16. (
            d'8 ]
         }
         {
            \time 2/8
            e'8 [
            f'8 ] )
         }
      }

   Function works on both leaves and containers.

   .. versionchanged:: 1.1.2
      renamed ``split.fractured_at_duration( )`` to
      ``componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners( )``.
   '''

   return _split_component_at_duration(component, prolated_duration, 
      spanners = 'fractured', tie_after = tie_after)
