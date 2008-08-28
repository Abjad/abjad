
def _remove_empty_containers(expr):
   '''Delete all emtpy sub-containers in expr.'''
   class Visitor(object):
      def visit(self, node):
         if node.kind('Container') and len(node) == 0:
            node._die( )
   v = Visitor( )
   expr._navigator._traverse(v)

