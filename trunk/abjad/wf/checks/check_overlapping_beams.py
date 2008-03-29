from abjad.helpers.instances import instances
from abjad.wf.tools import _report


def check_overlapping_beams(expr, report = True, ret = 'violators'):
   violators = [ ]
   for leaf in instances(expr, '_Leaf'):
      beams = leaf.spanners.get(classname = 'Beam')
      if len(beams) > 1:
         for beam in beams:
            if beam not in violators:
               violators.append(beam)
   total = len(expr.spanners.get(classname = 'Beam'))
   return _report(report, ret, violators, total, 'overlapping beam spanners.') 
