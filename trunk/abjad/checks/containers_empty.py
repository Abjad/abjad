from abjad.checks.check import _Check
from abjad.helpers.instances import instances


class ContainersEmpty(_Check):

   def _run(self, expr):
      from abjad.container.container import Container
      violators = [ ]
      bad, total = 0, 0
      for t in instances(expr, Container):
         if len(t) == 0:
            violators.append(t)
            bad += 1
         total += 1
      return violators, total
