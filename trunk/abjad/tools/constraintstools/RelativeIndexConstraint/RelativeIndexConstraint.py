from abjad.tools.constraintstools._Constraint._Constraint import _Constraint


class RelativeIndexConstraint(_Constraint):
    r'''A constraint for a relatively positioned group of items, i.e. every
    adjacent pair of two items.  The constraint is applied against the last
    possible grouping in a solution, with the understanding that it has been
    applied previously during each stage of the construction of that solution.

    ::

        abjad> from abjad.tools.constraintstools import RelativeIndexConstraint

    Instantiated from an integer representing a contiguous index range, or a 
    sequence of indices, and a function which takes as many arguments as
    indices were given:

    ::

        abjad> max_interval = RelativeIndexConstraint(2, lambda x, y: abs(x - y) < 3)

    The above constraint will only be applied against the last two items of
    any solution.

    ::

        abjad> max_interval([0, 2])
        True
        abjad> max_interval([1000, 0, 1])
        True
        abjad> max_interval([0, 0, 0, 0, 4])
        False

    ``RelativeIndexConstraints`` are immutable.

    Returns ``RelativeIndexConstraint`` instance.
    '''

    __slots__ = ('index_span', 'indices', 'procedure')

    def __init__(self, indices, procedure):
        if isinstance(indices, int):
            assert 1 < indices
            indices = range(indices)
        elif isinstance(indices, (list, tuple)):
            indices = sorted(set(indices))
            assert 1 < len(indices)
            min_indices = min(indices)
            indices = [x - min_indices for x in indices]
        else:
            raise Exception('Cannot determine indices from %s' % indices)
        object.__setattr__(self, 'indices', tuple(indices))
        object.__setattr__(self, 'index_span', max(indices) - min(indices) + 1)

        assert isinstance(procedure, type(lambda: None))
        assert procedure.func_code.co_argcount == len(indices)
        object.__setattr__(self, 'procedure', procedure)

    ### OVERRIDES ###

    def __call__(self, solution):
        if len(solution) < self.index_span:
            return True
        items = solution[-self.index_span:]
        return self.procedure(*[items[i] for i in self.indices])

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return '%r, %r' % (self.indices, self.procedure)
