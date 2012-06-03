from abjad.tools.abctools import AbjadObject


class _SolutionNode(AbjadObject):

    __slots__ = ('children', 'is_valid', 'parent', 'value')

    def __init__(self, value, parent=None, children=None):
        self.value = value
        self.parent = parent
        self.children = children
        self.is_valid = True

    ### OVERRIDES ###

    def __iter__(self):
        for x in self.children:
            yield x

    def __nonzero__(self):
        return self.valid

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.value)

    ### PUBLIC PROPERTIES ###        

    @property
    def depth(self):
        depth = 0
        node = self
        while node.parent is not None:
            depth += 1
            node = node.parent
        return depth
        
    @property
    def solution(self):
        node = self
        result = [node.value]
        while node.parent is not None:
            node = node.parent
            result.append(node.value)
        return tuple(reversed(result))

    ### PUBLIC METHODS ###

    def append(self, arg):
        self.children.append(arg)

    def extend(self, arg):
        self.children.extend(arg)

    def pop(self, i=-1):
        return self.children.pop(i)
