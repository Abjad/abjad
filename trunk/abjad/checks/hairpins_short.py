from abjad.checks.check import _Check


class HairpinsShort(_Check):
   '''Hairpins must span at least two leaves.'''

   def _run(self, expr):
      from abjad.hairpin.hairpin import _Hairpin
      violators = [ ]
      total, bad = 0, 0
      hairpins = [
         p for p in expr.spanners.contained if isinstance(p, _Hairpin)]
      for hairpin in hairpins:
         if len(hairpin.leaves) <= 1:
            violators.append(hairpin)
         total += 1
      return violators, total
