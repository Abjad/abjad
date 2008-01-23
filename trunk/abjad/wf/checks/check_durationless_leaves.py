from ... helpers.instances import instances
from .. tools import _report


def check_durationless_leaves(expr, report = True, ret = 'violators'):
   violators = [ ]
   leaves = instances(expr, 'Leaf')
   total, bad = 0, 0
   for leaf in leaves:
      total += 1
      if leaf.duration is None :
         violators.append(leaf)
         bad += 1
   return _report(report, ret, violators, total, 'leaves without duration.')
