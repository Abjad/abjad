def _traverse(expr, v):
   v.visit(expr)
   if isinstance(expr, (list, tuple)):
      for m in expr:
         _traverse(m, v)
   if hasattr(expr, '_music'):
      for m in expr._music:
         _traverse(m, v)
   if hasattr(v, 'unvisit'):
      v.unvisit(expr)


### TODO - replace with abjad.helpers.iterate ###
def instances(expr, classname):
   '''Return all class instances with classname in expr;
      works on score components, lists, tuples.'''
   class Visitor(object):
      def __init__(self, classname):
         self.classname = classname
         self.result = []
      def visit(self, node): 
         if hasattr(node, 'kind') and node.kind(classname):
            self.result.append(node)
   v = Visitor(classname)
   _traverse(expr, v)
   return v.result 
