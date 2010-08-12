from abjad.tools.componenttools._split_component_at_duration import _split_component_at_duration


def split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners(component, prolated_duration, tie_after = False):
   r'''Split `component` at `prolated_duration`.
   Leave spanners untouched.
   Return split parts. ::

      abjad> t = Staff(RigidMeasure((2, 8), notetools.make_repeated_notes(2)) * 2)
      abjad> macros.diatonicize(t)
      abjad> BeamSpanner(t[0])
      abjad> BeamSpanner(t[1])
      abjad> SlurSpanner(t.leaves)
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

      abjad> halves = componenttools.split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners(t.leaves[0], Rational(1, 32))
      abjad> f(t)
      \new Staff {
         {
            \time 2/8
            c'32 [ (
            c'16.
            d'8 ]
         }
         {
            \time 2/8
            e'8 [
            f'8 ] )
         }
      }

   Works on both leaves and containers.

   .. versionchanged:: 1.1.2
      renamed ``split.unfractured_at_duration( )`` to
      ``componenttools.split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners( )``.
   '''

   return _split_component_at_duration(component, prolated_duration, 
      spanners = 'unfractured', tie_after = tie_after)
