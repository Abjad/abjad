from abjad.checks.check import _Check

class HairpinsIntermarked(_Check):
   '''Are there any dynamic marks in the middle of a hairpin?'''

   def _run(self, expr):
      violators = [ ]
      total, bad = 0, 0
      for hairpin in expr.spanners.get(classname = '_Hairpin'):
         if len(hairpin) > 2:
            for leaf in hairpin[1 : -1]:
               if leaf.dynamics.mark:
                  violators.append(hairpin)
                  bad += 1
                  break
         total += 1
      return violators, total
