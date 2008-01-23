

def check_overlapping_glissandi(self, report = True, ret = 'violators'):
   '''Overlapping glissandi are a problem;
      dove-tailed glissandi are OK.'''
   violators = [ ] 
   for leaf in self._target.leaves:
      glissandi = leaf.glissando.spanners
      if len(glissandi) > 1:
         if len(glissandi) == 2:
            common_leaves = set(glissandi[0].leaves) & \
               set(glissandi[1].leaves)
            if len(common_leaves) == 1:
               x = list(common_leaves)[0]
               if (glissandi[0]._isMyFirstLeaf(x) and 
                  glissandi[1]._isMyLastLeaf(x)) or \
                  (glissandi[1]._isMyFirstLeaf(x) and 
                   glissandi[0]._isMyLastLeaf(x)):
                  break  

         for glissando in glissandi:
            if glissando not in violators:
               violators.append(glissando)
   bad = len(violators)
   total = len(self._target.spanners.get(classname = 'Glissando'))
   if report:
      print '%4d / %4d overlapping glissando spanners.' % (bad, total)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None
