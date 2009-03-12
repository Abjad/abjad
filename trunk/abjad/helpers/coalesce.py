#from abjad.helpers.hasname import hasname
from abjad.helpers.remove_empty_containers import _remove_empty_containers


def coalesce(expr): 
   '''Fuse all sub-containers in self that follow a thread.
      Function returns None if elements in expr are not threadable.'''

   from abjad.container.container import Container
   class Visitor(object):
      def __init__(self):
         self.merged = False
      def visit(self, node):
         #if hasname(node, 'Container'):
         if isinstance(node, Container):
            success = _fuse_right(node)
            if success:
               self.merged = True

   waslist = False
   if isinstance(expr, (list, tuple)):
      #from abjad.container.container import Container
      waslist = True
      expr = Container(expr)
   v = Visitor( )
   expr._navigator._traverse(v, depthFirst=False, leftRight=False)
   _remove_empty_containers(expr)
   if v.merged:
      if waslist:
         return expr.pop(0)
      else:
         return expr
                  

def _fuse_right(expr):
   '''Fuse expr with next container if next is threadable with self.'''
   next = expr._navigator._nextThread
   if next:
      expr.extend(next)
      next.detach( )
      return True
   else:
      return False
