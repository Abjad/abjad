from ... helpers.instances import instances
from .. tools import _report


def check_next_leaves(expr, report = True, ret = 'violators'):
   violators = [ ]
   leaves = instances(expr, 'Leaf')
   total, bad = 0, 0
   if leaves:
      leaves.pop( )
      total += 1
      for l in leaves:
         if not l.next:
            violators.append(l)
            bad += 1
         total += 1
   return _report(report, ret, violators, total, 'bad leaves.')
