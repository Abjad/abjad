from abjad.helpers.instances import instances
from abjad.wf.tools import _report


def check_overlapping_octavation(expr, report = True, ret = 'violators'):
   violators = [ ]
   for leaf in instances(expr, '_Leaf'):
      octavations = leaf.spanners.get(classname = 'Octavation')
      if len(octavations) > 1:
         for octavation in octavations:
            if octavation not in violators:
               violators.append(octavation)
   bad = len(violators)
   total = len(expr.spanners.get(classname = 'Octavation'))
   msg = 'overlapping octavation spanners.'
   return _report(report, ret, violators, total, msg)
