from abjad.exceptions import ExtraSpannerError
from abjad.tools import spannertools


def get_tie_chain(component):
   '''.. versionadded:: 1.1.2

   Get tie chain from `component`.
   '''

   tie_spanners = spannertools.get_all_spanners_attached_to_component(
      component, spannertools.TieSpanner)
   count = len(tie_spanners)

   if count == 0:
      return (component, )
   elif count == 1:
      return tuple(tie_spanners.pop( ).leaves)
   else:
      raise ExtraSpannerError
