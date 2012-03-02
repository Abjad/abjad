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

    __slots__ = ('_index_span', '_indices', '_predicate')

    def __init__(self, indices, predicate):
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
        object.__setattr__(self, '_indices', tuple(indices))
        object.__setattr__(self, '_index_span', max(indices) - min(indices) + 1)

        assert isinstance(predicate, type(lambda: None))
        assert predicate.func_code.co_argcount == 1
        object.__setattr__(self, '_predicate', predicate)

    ### OVERRIDES ###

    def __call__(self, solution):
        if len(solution) < self._index_span:
            return True

        items = solution[-self._index_span:]
        items = [items[i] for i in self._indices]
        counts = { }
        for x in items:
            if x not in counts:
                counts[x] = 1
            else:
                counts[x] += 1

        return self._predicate(counts)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return '%d, %r' % (self._indices, self._predicate)

    ### PUBLIC ATTRIBUTES ###

    @property
    def index_span(self):
        return self._index_span

    @property
    def indices(self):
        return self._indices

    @property
    def predicate(self):
        return self._predicate
