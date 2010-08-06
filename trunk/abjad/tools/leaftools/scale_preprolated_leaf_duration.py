from abjad.tools.leaftools.change_leaf_preprolated_duration import \
   change_leaf_preprolated_duration


def scale_preprolated_leaf_duration(leaf, multiplier):
   r'''Scale `leaf` preprolated duration by dotted `multiplier`::

      abjad> staff = Staff(macros.scale(4))
      abjad> Beam(staff.leaves)
      abjad> leaftools.scale_preprolated_leaf_duration(staff[1], Rational(3, 2))
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8.
         e'8
         f'8 ]
      }
      
   Scale `leaf` preprolated duration by tied `multiplier`::
      
      abjad> staff = Staff(macros.scale(4))
      abjad> Beam(staff.leaves)
      abjad> leaftools.scale_preprolated_leaf_duration(staff[1], Rational(5, 4))
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ~
         d'32
         e'8
         f'8 ]
      }
      
   Scale `leaf` preprolated duration by nonbinary `multiplier`::
      
      abjad> staff = Staff(macros.scale(4))
      abjad> Beam(staff.leaves)
      abjad> leaftools.scale_preprolated_leaf_duration(staff[1], Rational(2, 3))
      abjad> f(staff)
      \new Staff {
         c'8 [
         \times 2/3 {
            d'8
         }
         e'8
         f'8 ]
      }
      
   Scale `leaf` preprolated duration by tied nonbinary `multiplier`::
      
      abjad> staff = Staff(macros.scale(4))
      abjad> Beam(staff.leaves)
      abjad> leaftools.scale_preprolated_leaf_duration(staff[1], Rational(5, 6))
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

   .. versionchanged:: 1.1.2
      renamed ``leaftools.scale_leaf_preprolated_duration( )`` to
      ``leaftools.scale_preprolated_leaf_duration( )``.
   '''

   # find new leaf preprolated duration
   new_preprolated_duration = multiplier * leaf.duration.written

   # assign new leaf written duration and return structure
   return change_leaf_preprolated_duration(leaf, new_preprolated_duration)
