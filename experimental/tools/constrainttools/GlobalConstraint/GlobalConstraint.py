from experimental.tools.constrainttools._GlobalConstraint._GlobalConstraint \
    import _GlobalConstraint


class GlobalConstraint(_GlobalConstraint):
    r'''A constraint applied against an entire solution:

    ::

        >>> from experimental.tools.constrainttools import GlobalConstraint

    Instantiated from a function which takes a single argument, 
    representing an entire solution.

    ::

        >>> max_total_range = GlobalConstraint(
        ...     lambda seq: (max(seq) - min(seq)) < 5)

    ::

        >>> max_total_range([0, 1, 2])
        True
        >>> max_total_range([0, 1, 2, 3])
        True
        >>> max_total_range([0, 1, 2, 3, 4])
        True
        >>> max_total_range([0, 1, 2, 3, 4, 5])
        False

    ``GlobalConstraints`` are immutable.

    Returns ``GlobalConstraint`` instance.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, solution):
        return self._predicate(solution)
