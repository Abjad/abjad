from ... helpers.instances import instances
from .. tools import _report


def check_measures(expr, report = True, ret = 'violators'):
   violators = [ ]
   total, bad = 0, 0
   for p in instances(expr, 'Measure'):
      if not p.testDuration( ):
         violators.append(p)
         bad += 1
      total += 1
   return _report(report, ret, violators, total, 'bad measures.')
