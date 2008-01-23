from ... helpers.instances import instances
from .. tools import _report


def check_overlapping_glissandi(expr, report = True, ret = 'violators'):
   '''Overlapping glissandi are a problem;
      dove-tailed glissandi are OK.'''
   violators = [ ] 
   for leaf in instances(expr, 'Leaf'):
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
   total = len(expr.spanners.get(classname = 'Glissando'))
   msg = 'overlapping glissandi spanners.'
   return _report(report, ret, violators, total, msg)
