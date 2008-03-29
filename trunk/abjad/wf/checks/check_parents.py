from abjad.wf.tools import _report


def check_parents(expr, report = True, ret = 'violators'):
   '''
   Each node needs a parent;
   each node needs the *correct* parent.
   '''
   class Visitor(object):
      def __init__(self, target):
         self.parents = [target._parent]
         self.total = 0
         self.bad = 0
         self.violators = [ ]
      def visit(self, node):
         self.total += 1
         if node._parent != self.parents[-1]:
            self.bad += 1
            print '%s has parent %s instead of expected %s.\n' % (
               node, node._parent, self.parents[-1])
            self.violators.append(node)
         if hasattr(node, '_music'):
            self.parents.append(node)
      def unvisit(self, node):
         if hasattr(node, '_music'):
            self.parents.pop( )
   v = Visitor(expr)
   expr._navigator._traverse(v)
   return _report(report, ret, v.violators, v.total, 'missing parents.')
