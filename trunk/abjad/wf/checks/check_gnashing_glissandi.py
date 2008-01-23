from ... helpers.instances import instances
from .. tools import _report


def check_gnashing_glissandi(expr, report = True, ret = 'violators'):
   '''Glissando interface may set on 
      only last glissando spanner leaf.'''
   violators =  [ ]
   for leaf in instances(expr, 'Leaf'):
      if leaf.glissando:
         glissandi = leaf.glissando.spanners
         for glissando in glissandi:
            if not glissando._isMyLastLeaf(leaf):
               violators.append(leaf)
   total = len(expr.leaves)
   msg = 'gnashing glissando interface.'
   return _report(report, ret, violators, total, msg)
