from abjad.checks._Check import _Check


class MissingParentCheck(_Check):
    '''Each node except the root needs a parent.
        Each node needs the correct parent.'''

    def _run(self, expr):
        class Visitor(object):
            def __init__(self, target):
                self.parents = [target._parentage.parent]
                self.total = 0
                self.bad = 0
                self.violators = [ ]
            def visit(self, node):
                self.total += 1
                if node._parentage.parent != self.parents[-1]:
                    self.bad += 1
                    print '%s has parent %s instead of expected %s.\n' % (
                        node, node._parentage.parent, self.parents[-1])
                    self.violators.append(node)
                if hasattr(node, '_music'):
                    self.parents.append(node)
            def unvisit(self, node):
                if hasattr(node, '_music'):
                    self.parents.pop( )
        v = Visitor(expr)
        expr._navigator._traverse(v)
        return v.violators, v.total
