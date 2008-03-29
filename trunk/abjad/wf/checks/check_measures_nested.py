from abjad.helpers.instances import instances
from abjad.wf.tools import _report


def check_measures_nested(expr, report = True, ret = 'violators'):
   '''Do we have any nested measures?'''
   violators = [ ]
   total, bad = 0, 0
   for t in instances(expr, 'Measure'):
      if t._parentage._first('Measure'):
            violators.append(t)
            bad += 1
      total += 1
   return _report(report, ret, violators, total, 'nested measures.')
