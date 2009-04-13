from abjad.container.container import Container
from abjad.tools import componenttools


def remove_empty(expr):
   '''Delete all emtpy subcontainers in expr.'''

   class Visitor(object):
      def visit(self, node):
         if isinstance(node, Container) and len(node.leaves) == 0:
            componenttools.detach(node)

   v = Visitor( )
   expr._navigator._traverse(v, depthFirst = False)
