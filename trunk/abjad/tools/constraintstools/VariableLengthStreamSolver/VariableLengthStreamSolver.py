import random

from abjad.tools.constraintstools.Domain import Domain
from abjad.tools.constraintstools._Constraint._Constraint import _Constraint
from abjad.tools.constraintstools._SolutionNode._SolutionNode import _SolutionNode as Node
from abjad.tools.constraintstools._Solver._Solver import _Solver


class VariableLengthStreamSolver(_Solver):
    '''A solver which behaves similarly to the ``FiniteStreamSolver`` except that
    it can produce solutions of variable rather than fixed lengths.

    Instantiated from a Domain, a list of Constraints, and list of terminating
    constraints, which signal when to begin yielding solutions.

    This solver is best suited for generating solutions which sum to a fixed value,
    or whose solutions fall within a range of lengths.

    A poorly defined set of constraints can trigger infinite recursion, so care must
    be taken when constructing the problem to be explored.

    ::

        abjad> from abjad.tools.constraintstools import *
        abjad> domain = Domain([1, 2, 3, 4], 1)
        abjad> target_sum = GlobalConstraint(lambda x: sum(x) == 5)
        abjad> boundary_sum = GlobalConstraint(lambda x: sum(x) < 6)
        abjad> solver = VariableLengthStreamSolver(domain, [boundary_sum], [target_sum])
        abjad> for x in solver: x
        ...
        (1, 1, 1, 1, 1)
        (1, 1, 1, 2)
        (1, 1, 2, 1)
        (1, 1, 3)
        (1, 2, 1, 1)
        (1, 2, 2)
        (1, 3, 1)
        (1, 4)
        (2, 1, 1, 1)
        (2, 1, 2)
        (2, 2, 1)
        (2, 3)
        (3, 1, 1)
        (3, 2)
        (4, 1)
        
    ``VariableLengthStreamSolvers`` are immutable.

    Returns ``VariableLengthStreamSolver`` instance.
    '''

    def __init__(self, domain, constraints, terminators, randomized=False):
        assert isinstance(domain, Domain)
        assert all([isinstance(x, _Constraint) for x in constraints])
        assert all([isinstance(x, _Constraint) for x in terminators])
        object.__setattr__(self, '_domain', domain)
        object.__setattr__(self, '_constraints', tuple(constraints))
        object.__setattr__(self, '_terminators', tuple(terminators))
        object.__setattr__(self, '_randomized', bool(randomized))

    ### OVERRIDES ###

    def __iter__(self):
        if self._randomized:
            domain = self._domain.randomized()
        else:
            domain = self._domain
        constraints = self._constraints
        terminators = self._terminators

        def recurse(node):
            solution = node.solution

            # if the node does not fulfill constraints, 
            # we just pass - this is a dead end.
            if not all([constraint(solution) for constraint in constraints]):
                #node.invalidate( )
                pass

            else:

                # if we find a complete solution, yield it
                if all([terminator(solution) for terminator in terminators]):
                    yield solution

                # and if we find an incomplete solution,
                # create child nodes, and recurse into them.
                for x in domain[0]:
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
    def constraints(self):
        return self._constraints

    @property
    def domain(self):
        return self._domain

    @property
    def iterator(self):
        return self.__iter__()

    @property
    def randomized(self):
        return self._randomized

    @property
    def solutions(self):
        return [x for x in self.iterator]

    @property
    def terminators(self):
        return self._terminators
