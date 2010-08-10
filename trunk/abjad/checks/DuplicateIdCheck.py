from abjad.checks._Check import _Check
from abjad.components._Component import _Component
from abjad.tools import listtools


class DuplicateIDCheck(_Check):

   def _run(self, expr):
      from abjad.tools import iterate
      violators = [ ]
      components = iterate.naive_forward_in_expr(expr, _Component)
      total_ids = [id(x) for x in components]
      unique_ids = listtools.unique(total_ids)
      if len(total_ids) > len(unique_ids):
         for cur_id in unique_ids:
            if total_ids.count(cur_id) > 1:
               violators.extend([x for x in components if id(x) == cur_id])
      return violators, len(total_ids)
