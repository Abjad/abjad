

def check_gnashing_glissandi(self, report = True, ret = 'violators'):
   '''Glissando interface may set on 
      only last glissando spanner leaf.'''
   violators =  [ ]
   for leaf in self._target.leaves:
      if leaf.glissando:
         glissandi = leaf.glissando.spanners
         for glissando in glissandi:
            if not glissando._isMyLastLeaf(leaf):
               violators.append(leaf)
   bad = len(violators)
   total = len(self._target.leaves)
   if report:
      print '%4d / %4d gnashing glissando interfaces.' % (bad, total)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None
