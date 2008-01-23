

def check_overlapping_octavation(self, report = True, ret = 'violators'):
   violators = [ ]
   for leaf in self._target.leaves:
      octavations = leaf.spanners.get(classname = 'Octavation')
      if len(octavations) > 1:
         for octavation in octavations:
            if octavation not in violators:
               violators.append(octavation)
   bad = len(violators)
   total = len(self._target.spanners.get(classname = 'Octavation'))
   if report:
      print '%4d / %4d overlapping octavation spanners.' % (bad, total)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None 
