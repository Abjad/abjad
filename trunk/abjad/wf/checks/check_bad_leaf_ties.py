from abjad.helpers.instances import instances
from abjad.wf.tools import _report


def check_bad_leaf_ties(expr, report = True, ret = 'violators'):
   violators = [ ]
   leaves = instances(expr, '_Leaf')
   for leaf in leaves:
      if leaf.tie and leaf.next:
         if leaf.pitch != leaf.next.pitch:
            violators.append(leaf)
   total = len(leaves)
   return _report(report, ret, violators, total, 'leaves with bad ties.')
