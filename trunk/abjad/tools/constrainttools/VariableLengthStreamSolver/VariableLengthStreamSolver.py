import random

from abjad.tools.constrainttools.Domain import Domain
from abjad.tools.constrainttools._Constraint._Constraint import _Constraint
from abjad.tools.constrainttools._SolutionNode._SolutionNode import _SolutionNode as Node
from abjad.tools.constrainttools._Solver._Solver import _Solver


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

        abjad> from abjad.tools.constrainttools import *
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
        object.__setattr__(self, '_constraints', tuple(sorted(constraints, key=lambda x: x._sort_tuple)))
        object.__setattr__(self, '_terminators', tuple(sorted(terminators, key=lambda x: x._sort_tuple)))
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

            # if the node does not fulfill constraints, this is a dead end.
            # constraints are applied in order; we bail on first false result.
            valid = True
            for constraint in constraints:
                if not constraint(solution):  
                    valid = False
                    break

            if valid:

                # then we test terminators in the same manner
                for terminator in terminators:
                    if not terminator(solution):
                        valid = False
                        break

                if valid:                
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

    ### PUBLIC PROPERTIES ###

    @property
    def terminators(self):
        return self._terminators
