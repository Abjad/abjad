from abjad.container import Container
from abjad.tools import componenttools


def remove_empty(expr):
   r'''Remove empty containers in `expr`::

      abjad> staff = Staff(Container(construct.run(2)) * 4)
      abjad> pitchtools.diatonicize(staff.leaves)
      abjad> Beam(staff[:])
      abjad> containertools.contents_delete(staff[1])
      abjad> containertools.contents_delete(staff[-1])
      abjad> f(staff)
      \new Staff {
         {
            c'8 [
            d'8
         }
         {
         }
         {
            g'8
            a'8 ]
         }
         {
         }
      }
      
   ::
      
      abjad> containertools.remove_empty(staff)
   
   ::

      abjad> f(staff)
      \new Staff {
         {
            c'8 [
            d'8
         }
         {
            g'8
            a'8 ]
         }
      }

   Return none.
   '''

   class Visitor(object):
      def _visit(self, node):
         if isinstance(node, Container) and len(node.leaves) == 0:
            componenttools.remove_component_subtree_from_score_and_spanners([node])

   v = Visitor( )
   expr._navigator._traverse(v, depthFirst = False)
