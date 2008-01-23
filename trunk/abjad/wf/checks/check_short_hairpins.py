from .. tools import _report


def check_short_hairpins(expr, report = True, ret = 'violators'):
   violators = [ ]
   total, bad = 0, 0
   for hairpin in expr.spanners.get(classname = '_Hairpin'):
      if len(hairpin) <= 1:
         violators.append(hairpin)
      total += 1
   return _report(report, ret, violators, total, 'short hairpins')
