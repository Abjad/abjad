

def check_unrecognized_beams(self, report = True, ret = 'violators'):
   violators = [ ]
   leaves = self._target.leaves
   for leaf in leaves:
      if len(leaf.spanners.get(classname = 'Beam')) != \
         len(leaf.beam.spanners):
            violators.append(leaf)
   bad = len(violators)
   total = len(leaves)
   if report:
      print '%4d / %4d leaves with unrecognized beam spanners.' % (bad, total)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None 
