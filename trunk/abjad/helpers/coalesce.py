from abjad.helpers.assess_components import assess_components
from abjad.helpers.remove_empty_containers import _remove_empty_containers
from abjad.navigator.dfs import depth_first_search
from abjad.helpers.iterate import iterate

def coalesce(expr):
   '''Fuse containers in self that are strictly contiguous and have
   the same name.'''
   from abjad.container.container import Container
   from abjad.tuplet.tuplet import _Tuplet
   merged = False
   if not isinstance(expr, list):
      expr = [expr]
   expr = Container(expr)

   g = depth_first_search(expr, direction = 'right')
   for cmp in g:
      next = cmp._navigator._nextNamesake
      if isinstance(next, Container) and not next.parallel and \
         not isinstance(next, _Tuplet) and \
         assess_components([cmp, next], 'strict', 'score', False):
         cmp.extend(next)
         next.detach( )
         merged = True
   if merged:
      print expr
      _remove_empty_containers(expr)
      return expr.pop(0)
   else:
      return None

#def coalesce(expr): 
#   '''Fuse all sub-containers in self that follow a thread.
#      Function returns None if elements in expr are not threadable.'''
#
#   from abjad.container.container import Container
#   class Visitor(object):
#      def __init__(self):
#         self.merged = False
#      def visit(self, node):
#         if isinstance(node, Container):
#            success = _fuse_right(node)
#            if success:
#               self.merged = True
#
#   if not isinstance(expr, (list, tuple)):
#      expr = [expr]
#   expr = Container(expr)
#
#   v = Visitor( )
#   expr._navigator._traverse(v, depthFirst=False, leftRight=False)
#   _remove_empty_containers(expr)
#   if v.merged:
#      return expr.pop(0)
#   else:
#      print 'WARNING: nothing to coalesce.'
#      return None
#                  
#
#def _fuse_right(expr):
#   '''Fuse expr with next container if next is threadable with self.'''
#   from abjad.tuplet.tuplet import _Tuplet
#   next = expr._navigator._nextNamesake
#   if next and \
#      not expr.parallel and not isinstance(next, _Tuplet) and \
#      assess_components([expr, next], 'strict', 'score', False):
#      print next
#      expr.extend(next)
#      next.detach( )
#      return True
#   else:
#      return False

##def _fuse_right(expr):
##   '''Fuse expr with next container if next is threadable with self.'''
##   from abjad.tuplet.tuplet import _Tuplet
##   next = expr._navigator._nextThread
##   if next and not isinstance(next, _Tuplet):
##      expr.extend(next)
##      next.detach( )
##      return True
##   else:
##      return False
