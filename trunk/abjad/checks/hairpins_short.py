from abjad.checks.check import _Check


class HairpinsShort(_Check):
   '''Hairpins must span at least two leaves.'''

   def _run(self, expr):
      violators = [ ]
      total, bad = 0, 0
      for hairpin in expr.spanners.get(classname = '_Hairpin'):
         if len(hairpin) <= 1:
            violators.append(hairpin)
         total += 1
      return violators, total
