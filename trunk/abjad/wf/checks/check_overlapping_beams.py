

def check_overlapping_beams(self, report = True, ret = 'violators'):
   violators = [ ]
   for leaf in self._target.leaves:
      beams = leaf.spanners.get(classname = 'Beam')
      if len(beams) > 1:
         for beam in beams:
            if beam not in violators:
               violators.append(beam)
   bad = len(violators)
   total = len(self._target.spanners.get(classname = 'Beam'))
   if report:
      print '%4d / %4d overlapping beam spanners.' % (bad, total)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None 
