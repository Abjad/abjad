def _report(report, ret, violators, total, msg):
   bad = len(violators)
   if report:
      print '%4d / %4d %s' % (bad, total, msg)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None 
