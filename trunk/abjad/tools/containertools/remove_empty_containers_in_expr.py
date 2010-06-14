from abjad.container import Container
from abjad.tools.componenttools.remove_component_subtree_from_score_and_spanners import \
   remove_component_subtree_from_score_and_spanners


def remove_empty_containers_in_expr(expr):
   r'''Remove empty containers in `expr`::

      abjad> staff = Staff(Container(leaftools.make_repeated_notes(2)) * 4)
      abjad> pitchtools.diatonicize(staff.leaves)
      abjad> Beam(staff[:])
      abjad> containertools.delete_contents_of_container(staff[1])
      abjad> containertools.delete_contents_of_container(staff[-1])
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
      
      abjad> containertools.remove_empty_containers_in_expr(staff)
   
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

   .. versionchanged:: 1.1.2
      renamed ``containertools.remove_empty( )`` to
      ``containertools.remove_empty_containers_in_expr( )``.
   '''

   class Visitor(object):
      def _visit(self, node):
         if isinstance(node, Container) and len(node.leaves) == 0:
            remove_component_subtree_from_score_and_spanners([node])

   v = Visitor( )
   expr._navigator._traverse(v, depthFirst = False)
