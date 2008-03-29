from abjad.helpers.instances import instances
from abjad.wf.tools import _report


def check_containers(expr, report = True, ret = 'violators'):
   violators = [ ]
   containers = instances(expr, 'Container')
   bad, total = 0, 0
   for t in containers:
      if len(t) == 0:
         violators.append(t)
         bad += 1
      total += 1
   return _report(report, ret, violators, total, 'bad containers.')
