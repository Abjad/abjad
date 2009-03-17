from abjad.helpers.remove_empty_containers import _remove_empty_containers


def coalesce(expr): 
   '''Fuse all sub-containers in self that follow a thread.
      Function returns None if elements in expr are not threadable.'''

   from abjad.container.container import Container
   class Visitor(object):
      def __init__(self):
         self.merged = False
      def visit(self, node):
         if isinstance(node, Container):
            success = _fuse_right(node)
            if success:
               self.merged = True

   if not isinstance(expr, (list, tuple)):
      expr = [expr]
   expr = Container(expr)

   v = Visitor( )
   expr._navigator._traverse(v, depthFirst=False, leftRight=False)
   _remove_empty_containers(expr)
   if v.merged:
      return expr.pop(0)
   else:
      print 'WARNING: nothing to coalesce.'
      return None
                  

def _fuse_right(expr):
   '''Fuse expr with next container if next is threadable with self.'''
   from abjad.tuplet.tuplet import _Tuplet
   next = expr._navigator._nextThread
   if next and not isinstance(next, _Tuplet):
      expr.extend(next)
      next.detach( )
      return True
   else:
      return False
