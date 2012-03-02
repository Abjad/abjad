from abjad.tools.constraintstools._Constraint._Constraint import _Constraint


class RelativeCountsConstraint(_Constraint):
    '''A constraint which is applied against a dictionary whose keys are the 
    values in a set of items from a given solution, and whose values are the
    counts of those keys.  The constraint is always applied against the last
    possible group of items, and returns True automatically if the solution
    is of insufficient length.

    ::

        abjad> from abjad.tools.constraintstools import RelativeCountsConstraint

    Instantiated from an integer representing a contiguous index range, or a 
    sequence of indices, and a function which takes as many arguments as
    indices were given:

    ::

        abjad> test = lambda x: max(x.values( )) <= 2
        abjad> two_repeats_max = RelativeCountsConstraint([0, 1, 2], test)
        abjad> two_repeats_max([0])
        True
        abjad> two_repeats_max([0, 1, 2])
        True
        abjad> two_repeats_max([0, 0, 1])
        True
        abjad> two_repeats_max([0, 0, 0])
        False
    
    ``RelativeCountsConstraints`` are immutable.

    Returns ``RelativeCountsConstraint`` instance.
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
        assert procedure.func_code.co_argcount == 1
        object.__setattr__(self, 'procedure', procedure)

    ### OVERRIDES ###

    def __call__(self, solution):
        if len(solution) < self.index_span:
            return True

        items = solution[-self.index_span:]
        items = [items[i] for i in self.indices]
        counts = { }
        for x in items:
            if x not in counts:
                counts[x] = 1
            else:
                counts[x] += 1

        return self.procedure(counts)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return '%d, %r' % (self.slice_size, self.procedure)
