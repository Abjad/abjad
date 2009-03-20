def find(expr, name = None, klass = None):
   '''Search expr recursively for components with 
      name equal to 'name' and / or class name 'klass'.

      Return list of zero or more matching components in expr.

      'name' may be either an added attribute 
      (e.g. Component.name = 'name') or, in the case of contexts, 
      the name of the invocation (e.g. Context.invocation.name = 'name').

      For shallow traversal of container for numeric indices,
      use Container.__getitem__(i) instead.'''

   class Visitor(object):
      def __init__(self, name = name, klass = klass):
         self.klass = klass
         self.name = name
         self.result = [ ]
      def visit(self, node):
         namematch = True
         classmatch = True
         if self.name:
            if (hasattr(node, 'name') and self.name == node.name):   
               pass
            elif hasattr(node, 'invocation') and \
               node.invocation.name == self.name:
               pass
            else:
               namematch = False
         if self.klass: 
            if hasattr(node, 'invocation') and \
               node.invocation.type == self.klass:
               pass
            elif not isinstance(self.klass, str) and \
               isinstance(node, klass):
               pass
            else:
               classmatch = False
         if namematch and classmatch:
            self.result.append(node)

   v = Visitor(name, klass)
   expr._navigator._traverse(v)

   return v.result
