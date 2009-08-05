from abjad.container import Container
#from abjad.navigator.dfs import depth_first_search
from abjad.tools import check
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import iterate
from abjad.tuplet.tuplet import _Tuplet


def containers_by_reference(expr):
   '''Fuse containers in self that are strictly contiguous 
      and that have the same name.'''

   merged = False
   if not isinstance(expr, list):
      expr = [expr]
   expr = Container(expr)

   #g = depth_first_search(expr, direction = 'right')
   g = iterate.depth_first(expr, direction = 'right')
   for cmp in g:
      next = cmp._navigator._nextNamesake
      if isinstance(next, Container) and not next.parallel and \
         not isinstance(next, _Tuplet) and \
         check.assess_components([cmp, next], contiguity = 'strict', 
            share = 'score', allow_orphans = False):
         cmp.extend(next)
         componenttools.detach([next])
         merged = True
   if merged:
      print expr
      containertools.remove_empty(expr)
      return expr.pop(0)
   else:
      print 'debug did not merge'
      return None


## TODO implement containers_by_reference as a simple, non-recursive
## container fuser, like below:
#def containers_by_reference(expr):
#   '''Fuse containers in self that are strictly contiguous 
#      and that have the same name.'''
#   
#   check.assert_components(expr)
#
#   result = expr[0]
#   for cmp in expr[1:]:
#      if isinstance(cmp, Container) and not cmp.parallel:
#         componenttools.detach([cmp])
#         result.extend(cmp)
#   return result


