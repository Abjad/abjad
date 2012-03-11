from abjad.tools.constrainttools._GlobalConstraint._GlobalConstraint import _GlobalConstraint


class GlobalConstraint(_GlobalConstraint):
    r'''A constraint applied against an entire solution:

    ::

        abjad> from abjad.tools.constrainttools import GlobalConstraint

    Instantiated from a function which takes a single argument, representing an
    entire solution.

    ::

        abjad> max_total_range = GlobalConstraint(lambda seq: (max(seq) - min(seq)) < 5)

    ::

        abjad> max_total_range([0, 1, 2])
        True
        abjad> max_total_range([0, 1, 2, 3])
        True
        abjad> max_total_range([0, 1, 2, 3, 4])
        True
        abjad> max_total_range([0, 1, 2, 3, 4, 5])
        False

    ``GlobalConstraints`` are immutable.

    Returns ``GlobalConstraint`` instance.
    '''

    ### OVERRIDES ###

    def __call__(self, solution):
        return self._predicate(solution)


