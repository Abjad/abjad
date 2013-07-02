from experimental.tools.constrainttools._AbsoluteConstraint._AbsoluteConstraint \
    import _AbsoluteConstraint


class AbsoluteIndexConstraint(_AbsoluteConstraint):
    '''A constraint for an absolutely positioned item or group of items in a
    solution:

    ::

        >>> from experimental.tools.constrainttools import AbsoluteIndexConstraint

    Instantiated from an index, or sequence of indices, and a function which
    takes as many arguments as indices were given:

    ::

        >>> first_is_zero = AbsoluteIndexConstraint(0, lambda x: x == 0)
        >>> third_greater_than_second = AbsoluteIndexConstraint(
        ...     [1, 2], lambda x, y: x < y)

    ::

        >>> first_is_zero([0, 1, 2])
        True
        >>> first_is_zero([1, 12, 3, 4, 5])
        False

    ::

        >>> third_greater_than_second([0, 1, 2])
        True
        >>> third_greater_than_second([1, 12, 3, 4, 5])
        False

    ``AbsoluteIndexConstraints`` are immutable.

    Returns ``AbsoluteIndexConstraint`` instance.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, solution):
        if len(solution) < self._max_index + 1:
            return True
        return self._predicate(*[solution[i] for i in self._indices])
