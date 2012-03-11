from abjad.tools.constrainttools._RelativeConstraint._RelativeConstraint import _RelativeConstraint


class RelativeCountsConstraint(_RelativeConstraint):
    '''A constraint which is applied against a dictionary whose keys are the 
    values in a set of items from a given solution, and whose values are the
    counts of those keys.  The constraint is always applied against the last
    possible group of items, and returns True automatically if the solution
    is of insufficient length.

    ::

        abjad> from abjad.tools.constrainttools import RelativeCountsConstraint

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
