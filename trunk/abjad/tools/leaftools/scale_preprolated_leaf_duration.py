from abjad.tools.leaftools.set_preprolated_leaf_duration import set_preprolated_leaf_duration


def scale_preprolated_leaf_duration(leaf, multiplier):
   r'''.. versionadded:: 1.1.1
   
   Scale preprolated `leaf` leaf duration by dotted `multiplier`::

      abjad> staff = Staff(macros.scale(4))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> leaftools.scale_preprolated_leaf_duration(staff[1], Fraction(3, 2))
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8.
         e'8
         f'8 ]
      }
      
   Scale preprolated `leaf` duration by tied `multiplier`::
      
      abjad> staff = Staff(macros.scale(4))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> leaftools.scale_preprolated_leaf_duration(staff[1], Fraction(5, 4))
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ~
         d'32
         e'8
         f'8 ]
      }
      
   Scale preprolated `leaf` duration by nonbinary `multiplier`::
      
      abjad> staff = Staff(macros.scale(4))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> leaftools.scale_preprolated_leaf_duration(staff[1], Fraction(2, 3))
      abjad> f(staff)
      \new Staff {
         c'8 [
         \times 2/3 {
            d'8
         }
         e'8
         f'8 ]
      }
      
   Scale preprolated `leaf` duration by tied nonbinary `multiplier`::
      
      abjad> staff = Staff(macros.scale(4))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> leaftools.scale_preprolated_leaf_duration(staff[1], Fraction(5, 6))
      abjad> f(staff)
      \new Staff {
         c'8 [
         \times 2/3 {
            d'8 ~
            d'32
         }
         e'8
         f'8 ]
      }

   Return `leaf`.

   .. versionchanged:: 1.1.2
      renamed from ``leaftools.duration_scale( )``.
      ``leaftools.scale_preprolated_leaf_duration( )``.
   '''

   # find new leaf preprolated duration
   new_preprolated_duration = multiplier * leaf.duration.written

   # assign new leaf written duration and return structure
   return set_preprolated_leaf_duration(leaf, new_preprolated_duration)
