from abjad.checks.check import _Check
from abjad.tools import iterate
from abjad.tools import listtools


class IdsDuplicated(_Check):

   def _run(self, expr):
      from abjad.component.component import _Component
      violators = [ ]
      components = iterate.naive_forward(expr, _Component)
      total_ids = [id(x) for x in components]
      unique_ids = listtools.unique(total_ids)
      if len(total_ids) > len(unique_ids):
         for cur_id in unique_ids:
            if total_ids.count(cur_id) > 1:
               violators.extend([x for x in components if id(x) == cur_id])
      return violators, len(total_ids)
