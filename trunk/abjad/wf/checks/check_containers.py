

def check_containers(self, report = True, ret = 'violators'):
   violators = [ ]
   containers = instances(self._target, 'Container')
   bad, total = 0, 0
   for t in containers:
      if len(t) == 0:
         violators.append(t)
         bad += 1
      total += 1
   if report:
      print '%4d / %4d bad containers.' % (bad, total)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None
