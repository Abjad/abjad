

def check_beamed_quarters(self, report = True, ret = 'violators'):
   violators = [ ]
   leaves = self._target.leaves
   for leaf in leaves:
      if hasattr(leaf, 'beam') and leaf.beam.spanned:
         if leaf.beam.flags < 1:
            violators.append(leaf)
   bad = len(violators)
   total = len(leaves)
   if report:
      print '%4d / %4d quarter (or greater) durations in beam.' % (bad, total)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None 
