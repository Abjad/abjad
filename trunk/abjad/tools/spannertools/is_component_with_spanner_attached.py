
def is_component_with_spanner_attached(expr, klass = None):
   r'''.. versionadded:: 1.1.2

   True when `expr` is a component with spanner attached::

      abjad> staff = Staff(macros.scale(4))
      abjad> beam = spannertools.BeamSpanner(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8
         e'8
         f'8 ]
      }

   ::

      abjad> spannertools.is_component_with_spanner_attached(staff[0])
      True

   Otherwise false::
   
      abjad> spannertools.is_component_with_spanner_attached(staff)
      False

   When `klass` is not none then true when `expr` is a component
   with a spanner of `klass` attached.

   Return true or false.
   '''
   from abjad.components._Component import _Component

   if isinstance(expr, _Component):
      if klass is None:
         return 0 < len(expr.spanners.attached)
      else:
         for spanner in expr.spanners.attached:
            if isinstance(spanner, klass):
               return True
   return False
