from abjad.tools.constrainttools._Constraint._Constraint import _Constraint


class _AbsoluteConstraint(_Constraint):

    __slots__ = ('_indices', '_kind', '_max_index', '_predicate')

    def __init__(self, indices, predicate):
        object.__setattr__(self, '_kind', 'absolute')

        if isinstance(indices, int):
            assert 0 <= indices
            indices = [indices]
        elif isinstance(indices, (list, tuple)):
            indices = sorted(set(indices))
            assert all([0 <= x for x in indices])
        else:
            raise Exception('Cannot determine indices from %s' % indices)
        object.__setattr__(self, '_indices', indices)
        object.__setattr__(self, '_max_index', max(indices))

        assert isinstance(predicate, type(lambda: None))
        object.__setattr__(self, '_predicate', predicate)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return '%r, %r' % (self._indices, self._predicate)

    ### PUBLIC PROPERTIES ###

    @property
    def indices(self):
        return self._indices

    @property
    def max_index(self):
        return self._max_index
