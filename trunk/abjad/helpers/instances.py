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
def instances(expr, classtoken):
   '''Return all class instances with classtoken in expr;
      works on score components, lists, tuples.'''
   class Visitor(object):
      def __init__(self, classtoken):
         self.classtoken = classtoken
         self.result = []
      def visit(self, node): 
         if isinstance(node, classtoken):
            self.result.append(node)
   v = Visitor(classtoken)
   _traverse(expr, v)
   return v.result 
