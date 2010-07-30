from abjad.tools.parenttools._ignore import _ignore
from abjad.tools.parenttools._restore import _restore
from abjad.tools import spannertools
import copy


def clone_components_and_remove_all_spanners(components, n = 1):
   r'''Clone thread-contiguous `components` and remove any spanners.
   
   The steps taken by this function are as follows.
   Withdraw all components at any level in `components` from spanners.
   Deep copy unspanned components in `components`.
   Reapply spanners to all components at any level in `components`. ::
   
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

      abjad> result = componenttools.clone_components_and_remove_all_spanners(voice.leaves[2:4])
      abjad> result
      (Note(e', 8), Note(f', 8))

   ::

      abjad> new_voice = Voice(result)
      abjad> f(new_voice)
      \new Voice {
              e'8
              f'8
      }

   ::

      abjad> voice.leaves[2] is new_voice.leaves[0]
      False

   ::

      abjad> voice.leaves[2].beam.spanner is new_voice.leaves[0].beam.spanner
      False

   Clone `components` a total of `n` times. ::

      abjad> result = componenttools.clone_components_and_remove_all_spanners(voice.leaves[2:4], n = 3)
      abjad> result
      (Note(e', 8), Note(f', 8), Note(e', 8), Note(f', 8), Note(e', 8), Note(f', 8))

   ::

      abjad> new_voice = Voice(result)
      abjad> f(new_voice)
      \new Voice {
              e'8 
              f'8 
              e'8 
              f'8 
              e'8 
              f'8 
      }


   .. versionchanged:: 1.1.2
      renamed ``clone.unspan( )`` to
      ``componenttools.clone_components_and_remove_all_spanners( )``.
   '''
   from abjad.tools import componenttools

   if n < 1:
      return [ ]

   assert componenttools.all_are_thread_contiguous_components(components)

   spanners = spannertools.get_contained(components) 
   for spanner in spanners:
      spanner._block_all_components( )

   receipt = _ignore(components)

   result = copy.deepcopy(components)
   for component in result:
      component._update._markForUpdateToRoot( )

   _restore(receipt)

   for spanner in spanners:
      spanner._unblock_all_components( )

   for i in range(n - 1):
      result += clone_components_and_remove_all_spanners(components)
      
   return result
