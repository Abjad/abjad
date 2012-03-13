from abjad.tools.abctools import AbjadObject


class _SolutionNode(AbjadObject):

    __slots__ = ('_children', '_parent', '_valid', '_value')

    def __init__(self, value, parent = None):
        object.__setattr__(self, '_value', value)
        object.__setattr__(self, '_parent', parent)
        object.__setattr__(self, '_children', [ ])
        object.__setattr__(self, '_valid', True)

    ### OVERRIDES ###

    def __iter__(self):
        for x in self._children:
            yield x

    def __nonzero__(self):
        return self.valid

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.value)
        
    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    @property
    def solution(self):
        node = self
        result = [node.value]
        while node.parent is not None:
            node = node.parent
            result.append(node.value)
        return tuple(reversed(result))

    @property
    def valid(self):
        return self._valid

    @property
    def value(self):
        return self._value

    ### PUBLIC METHODS ###

    def append(self, arg):
        assert isinstance(arg, type(self))
        self._children.append(arg)

    def invalidate(self):
        object.__setattr__(self, '_valid', False)
