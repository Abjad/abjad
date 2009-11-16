from abjad.checks.check import _Check
from abjad.tools import iterate


class ContainersEmpty(_Check):

   runtime = 'composition'

   def _run(self, expr):
      from abjad.container import Container
      violators = [ ]
      bad, total = 0, 0
      for t in iterate.naive_forward_in(expr, Container):
         if len(t) == 0:
            violators.append(t)
            bad += 1
         total += 1
      return violators, total
