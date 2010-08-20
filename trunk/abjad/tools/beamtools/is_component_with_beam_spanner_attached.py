def is_component_with_beam_spanner_attached(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` is component with beam spanner attached.

   False otherwise.
   '''
   from abjad.components._Component import _Component
   from abjad.tools import spannertools

   if not isinstance(expr, _Component):
      return False
   
   return bool(spannertools.get_all_spanners_attached_to_component(expr, spannertools.BeamSpanner))
