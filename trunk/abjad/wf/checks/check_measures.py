

def check_measures(self, report = True, ret = 'violators'):
   violators = [ ]
   total, bad = 0, 0
   for p in instances(self._target, 'Measure'):
      if not p.testDuration( ):
         violators.append(p)
         bad += 1
      total += 1
   if report:
      print '%4d / %4d bad measures.' % (bad, total)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None
