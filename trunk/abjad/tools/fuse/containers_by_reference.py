from abjad.container import Container
from abjad.tools import check
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import iterate
from abjad.tuplet import _Tuplet


def containers_by_reference(expr):
   r'''Fuse like-named contiguous containers in `expr`::

      abjad> staff = Staff(Voice(leaftools.make_repeated_notes(2)) * 2)
      abjad> pitchtools.diatonicize(staff.leaves)
      abjad> staff[0].name = 'soprano'
      abjad> staff[1].name = 'soprano'
      abjad> f(staff)
      \new Staff {
         \context Voice = "soprano" {
            c'8
            d'8
         }
         \context Voice = "soprano" {
            e'8
            f'8
         }
      }
      
   ::
      
      abjad> fuse.containers_by_reference(staff)
      Staff{1}

   ::

      abjad> f(staff)
      \new Staff {
         \context Voice = "soprano" {
            c'8
            d'8
            e'8
            f'8
         }
      }

   Return `expr`.

   .. todo:: change interface to ``fuse.containers_by_name(staff[:])``
      to pass containers-to-be-fused explicitly.
   '''

   merged = False
   if not isinstance(expr, list):
      expr = [expr]
   expr = Container(expr)

   g = iterate.depth_first(expr, direction = 'right')
   for cmp in g:
      next = cmp._navigator._nextNamesake
      if isinstance(next, Container) and not next.parallel and \
         not isinstance(next, _Tuplet) and \
         check.assess_components([cmp, next], contiguity = 'strict', 
            share = 'score', allow_orphans = False):
         cmp.extend(next)
         componenttools.remove_component_subtree_from_score_and_spanners([next])
         merged = True
   if merged:
      #print expr
      containertools.remove_empty_containers_in_expr(expr)
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
#         componenttools.remove_component_subtree_from_score_and_spanners([cmp])
#         result.extend(cmp)
#   return result
