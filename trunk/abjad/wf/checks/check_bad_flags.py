#from ... helper.instances import instances
#from .. prepare import _prepare # wraps instances( )
from .. tools import _report


def check_bad_flags(expr, report = True, ret = 'violators'):
   violators = [ ]
   leaves = instances(expr, 'Leaf')
   for leaf in leaves:
      flags = leaf.beam.flags
      left, right = leaf.beam.counts
      if left is not None:
         if left > flags or (left < flags and right not in (flags, None)):
            if leaf not in violators:
               violators.append(leaf)
      if right is not None:
         if right > flags or (right < flags and left not in (flags, None)):
            if leaf not in violators:
               violators.append(leaf)
   bad = len(violators)
   total = len(leaves)
   _report(report, ret, bad, total, 'leaves with bad flags.')
