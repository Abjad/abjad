from abjad.tools import check
from abjad.tools import parenttools


def slip(components):
   r'''Remove arbitrary `components` from score 
   but retain children of `components` in score. ::

      abjad> staff = Staff(Container(construct.run(2)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> Slur(staff[:])
      abjad> Beam(staff.leaves)
      abjad> f(staff)
      \new Staff {
         {
            c'8 [ (
            d'8
         }
         {
            e'8
            f'8 ] )
         }
      }
      
   ::
      
      abjad> componenttools.slip(staff[0:1])
      [{ }]
      
   ::
      
      abjad> f(staff)
      \new Staff {
         c'8 [ (
         d'8
         {
            e'8
            f'8 ] )
         }
      }

   Return `components`.

   .. note:: should be renamed to 
      ``componenttools.remove_components_from_score_shallow( )``
   '''

   check.assert_components(components)
   for component in components:
      parent, start, stop = parenttools.get_with_indices([component])
      result = parent[start:stop+1] = list(component.music)
   return components
