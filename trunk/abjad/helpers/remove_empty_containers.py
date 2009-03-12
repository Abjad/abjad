def _remove_empty_containers(expr):
   '''Delete all emtpy sub-containers in expr.'''
   from abjad.container.container import Container
   class Visitor(object):
      def visit(self, node):
         if isinstance(node, Container) and len(node.leaves) == 0:
            node.detach( )
   v = Visitor( )
   expr._navigator._traverse(v, depthFirst = False)
