
def check_spanner_contiguity(self, report = True, ret = 'violators',
   interface = None, grob = None, attribute = None, value = None):
   violators = [ ]
   total, bad = 0, 0
   spanners = self._target.spanners.get(interface, grob, attribute, value)
   for spanner in spanners:
      contiguousLeaves = True
      leaves = spanner.leaves
      for i in range(len(leaves) - 1):
         if leaves[i].next != leaves[i + 1]:
            contiguousLeaves = False
      if not contiguousLeaves:
         violators.append(spanner)
         bad += 1
      total += 1
   if report:
      print '%4d / %4d bad spanners.' % (bad, total)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None 
