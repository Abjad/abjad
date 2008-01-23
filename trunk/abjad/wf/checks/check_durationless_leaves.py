

def check_durationless_leaves(self, report = True, ret = 'violators'):
   violators = [ ]
   leaves = instances(self._target, 'Leaf')
   total, bad = 0, 0
   for leaf in leaves:
      total += 1
      if leaf.duration is None :
         violators.append(leaf)
         bad += 1
   if report:
      print '%4d / %4d leaves without duration.' % (bad, total)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None
