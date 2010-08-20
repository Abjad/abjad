from abjad.tools.spannertools.get_all_spanners_attached_to_component import \
   get_all_spanners_attached_to_component


def get_all_spanners_attached_to_any_proper_children_of_component(component, klass = None):
   r'''.. versionadded:: 1.1.2

   Get all spanners attached to any proper children of `component`::

      abjad> staff = Staff(macros.scale(4))
      abjad> beam = spannertools.BeamSpanner(staff.leaves)
      abjad> first_slur = spannertools.SlurSpanner(staff.leaves[:2])
      abjad> second_slur = spannertools.SlurSpanner(staff.leaves[2:])
      abjad> trill = spannertools.TrillSpanner(staff)
      
   ::
      
      abjad> f(staff)
      \new Staff {
         c'8 [ ( \startTrillSpan
         d'8 )
         e'8 (
         f'8 ] ) \stopTrillSpan
      }

   ::

      abjad> spannertools.get_all_spanners_attached_to_any_proper_children_of_component(staff)
      set([BeamSpanner(c'8, d'8, e'8, f'8), SlurSpanner(c'8, d'8), CrescendoSpanner(c'8, d'8, e'8, f'8), SlurSpanner(e'8, f'8)])

   Get all spanners of `klass` attached to any proper children of `component`::

      abjad> spanner_klass = spannertools.SlurSpanner
      abjad> spannertools.get_all_spanners_attached_to_any_proper_children_of_component(staff, spanner_klass)
      set([SlurSpanner(c'8, d'8), SlurSpanner(e'8, f'8)])

   Get all spanners of any `klass` attached to any proper children of `component`::

      abjad> spanner_klasses = (spannertools.SlurSpanner, spannertools.BeamSpanner)
      abjad>spannertools.get_all_spanners_attached_to_any_proper_children_of_component(staff, spanner_klasses)
      set([BeamSpanner(c'8, d'8, e'8, f'8), SlurSpanner(c'8, d'8), SlurSpanner(e'8, f'8)])

   Return unordered set of zero or more spanners.
   '''
   from abjad.tools import componenttools

   ## note: externalization of (old) component spanner aggregator 'children' property
   result = set([ ])
   components = componenttools.iterate_components_forward_in_expr(component)

   ## remove component itself from iteration
   components.next( )
   
   ## iterate only proper children of component and save spanners
   for component in components:
      result.update(get_all_spanners_attached_to_component(component, klass))

   ## return result
   return result
