from ... duration.rational import Rational
from ... helpers.instances import instances
from .. tools import _report


def check_measures(expr, report = True, ret = 'violators'):
   violators = [ ]
   total, bad = 0, 0
   for t in instances(expr, 'Measure'):
      if t.meter is not None:
         if t.duration != Rational(*t.meter.pair):
            violators.append(t)
            bad += 1
      total += 1
   return _report(report, ret, violators, total, 'bad measures.')
