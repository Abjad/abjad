from .. tools import _report


def check_intermarked_hairpins(expr, report = True, ret = 'violators'):
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
   return _report(report, ret, violators, total, 'intermarked hairpins.')
