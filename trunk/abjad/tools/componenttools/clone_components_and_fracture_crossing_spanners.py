from abjad.component import _Component
from abjad.tools import iterate
from abjad.tools.parenttools._ignore import _ignore
from abjad.tools.parenttools._restore import _restore
from abjad.tools import spannertools
import copy


def clone_components_and_fracture_crossing_spanners(components, n = 1):
   r'''Clone thread-contiguous `components` and fracture 
   spanners that cover `components`.

   The steps this function takes are as follows.
   Deep copy `components`.
   Deep copy spanners that attach to any component in `components`.
   Fracture spanners that attach to components not in `components`.
   Return Python list of copied components. ::

      abjad> voice = Voice(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 3)
      abjad> pitchtools.diatonicize(voice)
      abjad> beam = Beam(voice.leaves[:4])
      abjad> f(voice)
      \new Voice {
              {
                      \time 2/8
                      c'8 [
                      d'8
              }
              {
                      \time 2/8
                      e'8
                      f'8 ]
              }
              {
                      \time 2/8
                      g'8
                      a'8
              }
      }

   ::

      abjad> result = componenttools.clone_components_and_fracture_crossing_spanners(voice.leaves[2:4])
      abjad> result
      (Note(e', 8), Note(f', 8))

   ::

      abjad> new_voice = Voice(result)
      abjad> f(new_voice)
      \new Voice {
              e'8 [
              f'8 ]
      }

   ::

      abjad> voice.leaves[2] is new_voice.leaves[0]
      False

   ::

      abjad> voice.leaves[2].beam.spanner is new_voice.leaves[0].beam.spanner
      False

   Clone `components` a total of `n` times. ::

      abjad> result = componenttools.clone_components_and_fracture_crossing_spanners(voice.leaves[2:4], n = 3)
      abjad> result
      (Note(e', 8), Note(f', 8), Note(e', 8), Note(f', 8), Note(e', 8), Note(f', 8))

   ::

      abjad> new_voice = Voice(result)
      abjad> f(new_voice)
      \new Voice {
              e'8 [
              f'8 ]
              e'8 [
              f'8 ]
              e'8 [
              f'8 ]
      }

   .. versionchanged:: 1.1.2
      renamed ``clone.fracture( )`` to
      ``componenttools.clone_components_and_fracture_crossing_spanners( )``.
   '''
   from abjad.tools import componenttools

   if n < 1:
      return [ ]

   assert componenttools.all_are_thread_contiguous_components(components)

   selection_components = set(iterate.naive_forward_in_expr(components, _Component))

   spanners = spannertools.get_spanners_that_cross_components(components) 

   spanner_map = set([ ])
   for spanner in spanners:
      spanner_map.add((spanner, tuple(spanner[:])))
      for component in spanner[:]:
         if component not in selection_components:
            spanner._remove_component(component)

   receipt = _ignore(components)
   
   result = copy.deepcopy(components)

   for component in result:
      component._update._mark_for_update_to_root( )

   _restore(receipt)

   for spanner, contents in spanner_map:
      spanner.clear( )
      spanner.extend(list(contents))

   for i in range(n - 1):
      result += clone_components_and_fracture_crossing_spanners(components)

   return result
