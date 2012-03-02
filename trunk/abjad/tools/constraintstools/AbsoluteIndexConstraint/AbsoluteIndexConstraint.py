from abjad.tools.constraintstools._Constraint._Constraint import _Constraint


class AbsoluteIndexConstraint(_Constraint):
    '''A constraint for an absolutely positioned item or group of items in a
    solution:

    ::

        abjad> from abjad.tools.constraintstools import AbsoluteIndexConstraint

    Instantiated from an index, or sequence of indices, and a function which
    takes as many arguments as indices were given:

    ::

        abjad> first_is_zero = AbsoluteIndexConstraint(0, lambda x: x == 0)
        abjad> third_greater_than_second = AbsoluteIndexConstraint([1, 2], lambda x, y: x < y)

    ::

        abjad> first_is_zero([0, 1, 2])
        True
        abjad> first_is_zero([1, 12, 3, 4, 5])
        False

    ::

        abjad> third_greater_than_second([0, 1, 2])
        True
        abjad> third_greater_than_second([1, 12, 3, 4, 5])
        False

    ``AbsoluteIndexConstraints`` are immutable.

    Returns ``AbsoluteIndexConstraint`` instance.
    '''

    __slots__ = ('_indices', '_max_index', '_predicate')

    def __init__(self, indices, predicate):
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
        assert predicate.func_code.co_argcount == len(indices)
        object.__setattr__(self, '_predicate', predicate)

    ### OVERRIDES ###

    def __call__(self, solution):
        if len(solution) < self._max_index + 1:
            return True
        return self._predicate(*[solution[i] for i in self._indices])

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return '%r, %r' % (self._indices, self._predicate)

    ### PUBLIC ATTRIBUTES ###

    @property
    def indices(self):
        return self._indices

    @property
    def max_index(self):
        return self._max_index

    @property
    def predicate
        return self._predicate
