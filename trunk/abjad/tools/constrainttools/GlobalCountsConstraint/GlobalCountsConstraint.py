from abjad.tools.constrainttools._GlobalConstraint._GlobalConstraint import _GlobalConstraint


class GlobalCountsConstraint(_GlobalConstraint):
    '''A constraint which is applied against a dictionary whose keys are the 
    values in a given solution, and whose values are the counts of those keys:

    ::

        abjad> from abjad.tools.constrainttools import GlobalCountsConstraint

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

    ### OVERRIDES ###

    def __call__(self, solution):
        counts = { }
        for x in solution:
            if x not in counts:
                counts[x] = 1
            else:
                counts[x] += 1
        return self._predicate(counts)
