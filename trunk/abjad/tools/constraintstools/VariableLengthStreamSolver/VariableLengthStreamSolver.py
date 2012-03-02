import random

from abjad.tools.constraintstools.Domain import Domain
from abjad.tools.constraintstools._Constraint._Constraint import _Constraint
from abjad.tools.constraintstools._SolutionNode._SolutionNode import _SolutionNode as Node


class VariableLengthStreamSolver(object):
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

    def __init__(self, domain, constraints, terminators, randomize=False):
        assert isinstance(domain, Domain)
        assert all([isinstance(x, _Constraint) for x in constraints])
        assert all([isinstance(x, _Constraint) for x in terminators])
        self._domain = domain
        self._constraints = tuple(constraints)
        self._terminators = tuple(terminators)
        self._randomize = bool(randomize)

    ### OVERRIDES ###

    def __iter__(self):
        if self._randomize:
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
    def solutions(self):
        return [x for x in self.iterator]

    @property
    def iterator(self):
        return self.__iter__()
