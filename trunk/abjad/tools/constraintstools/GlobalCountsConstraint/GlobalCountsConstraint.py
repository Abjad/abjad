from abjad.tools.constraintstools._Constraint._Constraint import _Constraint


class GlobalCountsConstraint(_Constraint):
    '''A constraint which is applied against a dictionary whose keys are the 
    values in a given solution, and whose values are the counts of those keys:

    ::

        abjad> from abjad.tools.constraintstools import GlobalCountsConstraint

    Instantiated from a lambda or function which takes a dictionary as its one
    and only argument:

    ::

        abjad> all_unique = GlobalCountsConstraint(lambda x: all([y == 1 for y in x.values()]))
        abjad> one_climax = GlobalCountsConstraint(lambda x: x[max(x.keys())] == 1)

    ::

        abjad> all_unique([1, 2, 3, 4, 0, -1])
        True
        abjad> all_unique([1, 1, 2, 3, 4, 0, -1])
        False

    ::

        abjad> one_climax([1, 2, 3, 4, 0, -1])
        True
        abjad> one_climax([1, 5, 5, 3])
        False

    ``GlobalCountsConstraints`` are immutble.

    Returns ``GlobalCountsConstraint`` instance.
    '''

    __slots__ = ('_predicate')

    def __init__(self, predicate):
        assert isinstance(predicate, type(lambda: None))
        assert predicate.func_code.co_argcount == 1
        object.__setattr__(self, '_predicate', predicate)

    ### OVERRIDES ###

    def __call__(self, solution):
        counts = { }
        for x in solution:
            if x not in counts:
                counts[x] = 1
            else:
                counts[x] += 1
        return self._predicate(counts)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return '%r' % self._predicate

    ### PUBLIC ATTRIBUTES ###

    @property
    def predicate(self):
        return self._predicate
