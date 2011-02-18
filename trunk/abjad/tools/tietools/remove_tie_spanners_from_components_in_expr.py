from abjad.tools import spannertools


def remove_tie_spanners_from_components_in_expr(expr):
   r'''Remove tie spanners components in `expr`::

      abjad> staff = Staff(macros.scale(2, (5, 16)))
      abjad> f(staff)
      \new Staff {
         c'4 ~
         c'16
         d'4 ~
         d'16
      }
      
   ::
      
      abjad> tietools.remove_tie_spanners_from_components_in_expr(staff[:])
      abjad> f(staff)
      \new Staff {
         c'4
         c'16
         d'4
         d'16
      }

   Return `expr`.

   .. versionchanged:: 1.1.2
      renamed ``componenttools.untie_shallow( )`` to
      ``tietools.remove_tie_spanners_from_components_in_expr( )``.
   '''
   from abjad.tools import componenttools

   for component in componenttools.iterate_components_forward_in_expr(expr):
      spannertools.destroy_all_spanners_attached_to_component(component, spannertools.TieSpanner)

   return expr
