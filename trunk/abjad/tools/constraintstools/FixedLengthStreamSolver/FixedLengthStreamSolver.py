import random

from abjad.tools.constraintstools.Domain import Domain
from abjad.tools.constraintstools._Constraint._Constraint import _Constraint
from abjad.tools.constraintstools._SolutionNode._SolutionNode import _SolutionNode as Node


class FixedLengthStreamSolver(object):
    r'''Recursive tree-traversal-based finite-domain constraints solver:

    ::

        abjad> from abjad.tools.constraintstools import FixedLengthStreamSolver
        abjad> from abjad.tools.constraintstools import Domain
        abjad> from abjad.tools.constraintstools import GlobalCountsConstraint
        abjad> from abjad.tools.constraintstools import RelativeIndexConstraint

    Instantiates from a ``Domain``, and a sequence of ``Constraints``.

    ::

        abjad> domain = Domain([1, 2, 3, 4], 4)
        abjad> all_unique = GlobalCountsConstraint(lambda x: all([y == 1 for y in x.values()]))
        abjad> max_interval = RelativeIndexConstraint([0, 1], lambda x, y: abs(x - y) < 3)
        abjad> solver = FixedLengthStreamSolver(domain, [all_unique, max_interval])

    Generate solutions by iterating over the ``FixedLengthStreamSolver``.

    ::

        abjad> for solution in solver: print solution
        ... 
        (1, 2, 3, 4)
        (1, 2, 4, 3)
        (1, 3, 2, 4)
        (1, 3, 4, 2)
        (2, 1, 3, 4)
        (2, 4, 3, 1)
        (3, 1, 2, 4)
        (3, 4, 2, 1)
        (4, 2, 1, 3)
        (4, 2, 3, 1)
        (4, 3, 1, 2)
        (4, 3, 2, 1)

    If no solutions can be found, returns none:

    ::

        abjad> domain = Domain([1, 2, 3, 4], 100)
        abjad> solver = FixedLengthStreamSolver(domain, [all_unique])
        abjad> [x for x in solver]
        []

    Can be instantiated with boolean ``randomize`` keyword, in order to
    randomize the domain on each iteration run:

    ::

        abjad> random_solver = FixedLengthStreamSolver(domain, [all_unique, max_interval], randomize=True)

    ``FixedLengthStreamSolvers`` are immutable.

    Returns ``FixedLengthStreamSolver`` instance.
    '''

    def __init__(self, domain, constraints, randomize=False):
        assert isinstance(domain, Domain)
        assert all([isinstance(x, _Constraint) for x in constraints])
        self._domain = domain
        self._constraints = tuple(constraints)
        self._randomize = bool(randomize)

    ### OVERRIDES ###

    def __iter__(self):
        if self._randomize:
            domain = self._domain.randomized()
        else:
            domain = self._domain
        constraints = self._constraints

        def recurse(node):
            solution = node.solution

            # if the node does not fulfill constraints, 
            # we just pass - this is a dead end.
            if not all([constraint(solution) for constraint in constraints]):
                #node.invalidate( )
                pass

            # if we find a complete solution, yield it
            elif len(solution) == len(domain):
                yield solution

            # and if we find an incomplete solution,
            # create child nodes, and recurse into them.
            else:
                for x in domain[len(solution)]:
                    child = Node(x, node)
                    node.append(child)
                    for y in recurse(child):
                        yield y

        for x in domain[0]:
            node = Node(x)
            for y in recurse(node):
                yield y

    ### PUBLIC ATTRIBUTES ###

    @property
    def solutions(self):
        return [x for x in self.iterator]

    @property
    def iterator(self):
        return self.__iter__()
