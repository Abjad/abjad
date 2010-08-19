def get_all_spanners_attached_to_component(component, klass = None):
   r'''.. versionadded:: 1.1.2

   Get all spanners attached to `component`::

      abjad> staff = Staff(macros.scale(4))
      abjad> beam = spannertools.BeamSpanner(staff.leaves)
      abjad> first_slur = spannertools.SlurSpanner(staff.leaves[:2])
      abjad> second_slur = spannertools.SlurSpanner(staff.leaves[2:])
      abjad> crescendo = spannertools.CrescendoSpanner(staff.leaves)

   ::

      abjad> f(staff)
      \new Staff {
         c'8 [ \< (
         d'8 )
         e'8 (
         f'8 ] \! )
      }

   ::

      abjad> spannertools.get_spanners_attached_to_component(staff.leaves[0])
      set([BeamSpanner(c'8, d'8, e'8, f'8), SlurSpanner(c'8, d'8), CrescendoSpanner(c'8, d'8, e'8, f'8)])

   Get spanners of `klass` attached to `component`::

      abjad> klass = spannertools.BeamSpanner
      abjad> spannertools.get_spanners_attached_to_component(staff.leaves[0], klass)
      set([BeamSpanner(c'8, d'8, e'8, f'8)])

   Get spanners of any `klass` attached to `component`::

      abjad> klasses = (spannertools.BeamSpanner, spannertools.SlurSpanner)
      abjad> spannertools.get_spanners_attached_to_component(staff.leaves[0], klasses)
      set([BeamSpanner(c'8, d'8, e'8, f'8), SlurSpanner(c'8, d'8)])

   Return unordered set of zero or more spanners.
   '''

   ## note: externalization of (old) component spanner aggregator 'spanners' property
   if klass is None:
      return set(component.spanners.attached)
   else:
      return set([x for x in component.spanners.attached if isinstance(x, klass)])
