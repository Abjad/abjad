from ... helpers.instances import instances
from ... helpers.unique import unique
from .. tools import _report


def check_duplicate_ids(expr, report = True, ret = 'violators'):
   violators = [ ]
   components = instances(expr, '_Component')
   total_ids = [id(x) for x in components]
   unique_ids = unique(total_ids)
   if len(total_ids) > len(unique_ids):
      for cur_id in unique_ids:
         if total_ids.count(cur_id) > 1:
            violators.extend([x for x in components if id(x) == cur_id])
   total = len(total_ids)
   return _report(report, ret, violators, total, 'duplicate component ids.')
