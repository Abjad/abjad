from abjad.components._Component import _Component
from abjad.tools import spannertools


def is_component_with_tie_spanner_attached(expr):
   r'''.. versionadded:: 1.1.2

   True when `expr` is component with tie spanner attached::

      abjad> staff = Staff(notetools.make_repeated_notes(4))
      abjad> spannertools.TieSpanner(staff[:])
      abjad> f(staff)
      \new Staff {
         c'8 ~
         c'8 ~
         c'8 ~
         c'8
      }
      abjad> tietools.is_component_with_tie_spanner_attached(staff)
      True

   Otherwise false::

      abjad> staff = Staff(notetools.make_repeated_notes(4))
      abjad> spannertools.TieSpanner(staff[:])
      abjad> f(staff)
      \new Staff {
         c'8 ~
         c'8 ~
         c'8 ~
         c'8
      }
      abjad> tietools.is_component_with_tie_spanner_attached(t[1])
      False
   '''

   if not isinstance(expr, _Component):
      return False
   
   return bool(spannertools.get_all_spanners_attached_to_component(
      expr, spannertools.TieSpanner))
