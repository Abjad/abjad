

def check_short_hairpins(self, report = True, ret = 'violators'):
   violators = [ ]
   total, bad = 0, 0
   for hairpin in self._target.spanners.get(classname = '_Hairpin'):
      if len(hairpin) <= 1:
         violators.append(hairpin)
         bad += 1
      total += 1
   if report:
      print '%4d / %4d short hairpins.' % (bad, total)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None 
