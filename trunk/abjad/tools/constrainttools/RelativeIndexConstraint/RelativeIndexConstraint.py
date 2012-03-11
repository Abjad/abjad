from abjad.tools.constrainttools._RelativeConstraint._RelativeConstraint import _RelativeConstraint


class RelativeIndexConstraint(_RelativeConstraint):
    r'''A constraint for a relatively positioned group of items, i.e. every
    adjacent pair of two items.  The constraint is applied against the last
    possible grouping in a solution, with the understanding that it has been
    applied previously during each stage of the construction of that solution.

    ::

        abjad> from abjad.tools.constrainttools import RelativeIndexConstraint

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

    ### OVERRIDES ###

    def __call__(self, solution):
        if len(solution) < self._index_span:
            return True
        items = solution[-self._index_span:]
        return self._predicate(*[items[i] for i in self._indices])
