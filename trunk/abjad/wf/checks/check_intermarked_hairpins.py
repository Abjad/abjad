

def check_intermarked_hairpins(self, report = True, ret = 'violators'):
   violators = [ ]
   total, bad = 0, 0
   for hairpin in self._target.spanners.get(classname = '_Hairpin'):
      if len(hairpin) > 2:
         for leaf in hairpin.leaves[1 : -1]:
            if leaf.dynamics.mark:
               violators.append(hairpin)
               bad += 1
               break
      total += 1
   if report:
      print '%4d / %4d intermarked hairpins.' % (bad, total)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None 
