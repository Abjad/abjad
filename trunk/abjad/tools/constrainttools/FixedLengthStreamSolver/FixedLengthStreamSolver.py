import random

from abjad.tools.constrainttools.Domain import Domain
from abjad.tools.constrainttools._Constraint._Constraint import _Constraint
from abjad.tools.constrainttools._SolutionNode._SolutionNode import _SolutionNode as Node
from abjad.tools.constrainttools._Solver._Solver import _Solver


class FixedLengthStreamSolver(_Solver):
    r'''Recursive tree-traversal-based finite-domain constraints solver:

    ::

        >>> from abjad.tools.constrainttools import FixedLengthStreamSolver
        >>> from abjad.tools.constrainttools import Domain
        >>> from abjad.tools.constrainttools import GlobalCountsConstraint
        >>> from abjad.tools.constrainttools import RelativeIndexConstraint

    Instantiates from a ``Domain``, and a sequence of ``Constraints``.

    ::

        >>> domain = Domain([1, 2, 3, 4], 4)
        >>> all_unique = GlobalCountsConstraint(lambda x: all([y == 1 for y in x.values()]))
        >>> max_interval = RelativeIndexConstraint([0, 1], lambda x, y: abs(x - y) < 3)
        >>> solver = FixedLengthStreamSolver(domain, [all_unique, max_interval])

    Generate solutions by iterating over the ``FixedLengthStreamSolver``.

    ::

        >>> for solution in solver: print solution
        ... 
        [1, 2, 3, 4]
        [1, 2, 4, 3]
        [1, 3, 2, 4]
        [1, 3, 4, 2]
        [2, 1, 3, 4]
        [2, 4, 3, 1]
        [3, 1, 2, 4]
        [3, 4, 2, 1]
        [4, 2, 1, 3]
        [4, 2, 3, 1]
        [4, 3, 1, 2]
        [4, 3, 2, 1]

    If no solutions can be found, returns none:

    ::

        >>> domain = Domain([1, 2, 3, 4], 100)
        >>> solver = FixedLengthStreamSolver(domain, [all_unique])
        >>> [x for x in solver]
        []

    Can be instantiated with boolean ``randomized`` keyword, in order to
    randomize the domain on each iteration run:

    ::

        >>> random_solver = FixedLengthStreamSolver(domain, [all_unique, max_interval], randomized=True)

    ``FixedLengthStreamSolvers`` are immutable.

    Returns ``FixedLengthStreamSolver`` instance.
    '''

    __slots__ = ('_constraints', '_domain', '_randomized')

    def __init__(self, domain, constraints, randomized=False):
        assert isinstance(domain, Domain)
        assert all([isinstance(x, _Constraint) for x in constraints])
        object.__setattr__(self, '_domain', domain)
        object.__setattr__(self, '_constraints', tuple(sorted(constraints, key=lambda x: x._sort_tuple)))
        object.__setattr__(self, '_randomized', bool(randomized))

    ### SPECIAL METHODS ###

    def __iter__(self):

        domain = self._domain
        domain_length = len(domain)
        constraints = self._constraints

        def random_recurse(node, prev_solution, prev_depth=0):
            depth = prev_depth + 1
            solution = list(prev_solution) + [node.value]
            valid = True
            for constraint in constraints:
                if not constraint(solution):
                    valid = False
                    break
            if valid:
                if depth == domain_length:
                    return solution, node
                else:
                    if node.children is None:
                        node.children = [Node(x, parent=node) for x in domain[depth]]
                    elif node.children == []:
                        return node
                    else:
                        result = random_recurse(random.choice(node.children), solution, depth)
                        if isinstance(result, list):
                            return result
                        if isinstance(result, tuple):
                            solution, child = result
                            node.children.remove(child)
                            if node.children == []:
                                return solution, node
                            return solution
                        elif result is None:
                            return None
                        elif isinstance(result, type(node)):
                            node.children.remove(result)
                            if node.children == []:
                                return node    
                            return None
            else:
                return node

        def ordered_recurse(node, prev_solution, prev_depth=0):
            depth = prev_depth + 1
            solution = list(prev_solution) + [node.value]
            valid = True
            for constraint in constraints:
                if not constraint(solution):
                    valid = False
                    break
            if valid:
                if depth == domain_length:
                    yield solution
                else:
                    for x in domain[depth]:
                        child = Node(x, parent=node, children=[])
                        node.append(child)
                        for y in ordered_recurse(child, solution, depth):
                            yield y

        # randomized traversal
        if self.randomized:
            graphs = [Node(x) for x in domain[0]]
            while graphs:
                result = random_recurse(random.choice(graphs), [], 0)
                if isinstance(result, list):
                    yield result
                elif isinstance(result, tuple):
                    solution, node = result
                    graphs.remove(node)
                    yield solution
                elif isinstance(result, Node):
                    graphs.remove(result)

        # ordered traversal
        else:
            for x in domain[0]:
                node = Node(x, children=[])
                for y in ordered_recurse(node, [], 0):
                    yield y
