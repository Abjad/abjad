

def check_next_leaves(self, report = True, ret = 'violators'):
   violators = [ ]
   leaves = self._target.leaves
   total, bad = 0, 0
   if leaves:
      leaves.pop( )
      total += 1
      for l in leaves:
         if not l.next:
            violators.append(l)
            bad += 1
         total += 1
   if report:
      print '%4d / %4d bad leaves.' % (bad, total)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None
