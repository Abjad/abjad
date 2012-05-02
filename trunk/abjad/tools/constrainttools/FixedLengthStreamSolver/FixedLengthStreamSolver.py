import random

from abjad.tools.constrainttools.Domain import Domain
from abjad.tools.constrainttools._Constraint._Constraint import _Constraint
from abjad.tools.constrainttools._SolutionNode._SolutionNode import _SolutionNode as Node
from abjad.tools.constrainttools._Solver._Solver import _Solver


class FixedLengthStreamSolver(_Solver):
    r'''Recursive tree-traversal-based finite-domain constraints solver:

    ::

        abjad> from abjad.tools.constrainttools import FixedLengthStreamSolver
        abjad> from abjad.tools.constrainttools import Domain
        abjad> from abjad.tools.constrainttools import GlobalCountsConstraint
        abjad> from abjad.tools.constrainttools import RelativeIndexConstraint

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

        abjad> domain = Domain([1, 2, 3, 4], 100)
        abjad> solver = FixedLengthStreamSolver(domain, [all_unique])
        abjad> [x for x in solver]
        []

    Can be instantiated with boolean ``randomized`` keyword, in order to
    randomize the domain on each iteration run:

    ::

        abjad> random_solver = FixedLengthStreamSolver(domain, [all_unique, max_interval], randomized=True)

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

    ### OVERRIDES ###

    def __iter__(self):

        domain = self._domain
        domain_length = len(domain)
        constraints = self._constraints

        def random_recurse(node, prev_solution):
	
            solution = list(prev_solution) + [node.value]

            valid = True
            for constraint in constraints:
                if not constraint(solution):
                    valid = False
                    break

            if valid:
                if len(solution) == domain_length:
                    # we found a solution
                    return solution, node

                else:
                    if node.children is None:
                        depth = node.depth + 1
                        node.children = [Node(x, parent=node) for x in domain[depth]]

                    elif node.children == []:
                        return node

                    else:
                        result = random_recurse(random.choice(node.children), solution)

                        # if list, then we've found a result, propogate it up the chain
                        if isinstance(result, list):
                            return result

                        # if tuple, we have a pair of solution and terminal node
                        # we need to remove the terminal node (and any subsequently terminal parent node)
                        # so that later random descents do not repeat this same traversal
                        if isinstance(result, tuple):
                            solution, child = result
                            node.children.remove(child)
                            if node.children == []:
                                return solution, node
                            return solution

                        # if None, we found a deadend somewhere earlier
                        elif result is None:
                            return None

                        # if a node, it must be removed from this node's children list
                        # then, if the children list is empty, this node is also a deadend
                        # in which case, we return this node and repeat the process
                        elif isinstance(result, type(node)):
                            node.children.remove(result)
                            if node.children == []:
                                return node    
                            return None

            else:
                return node

        def ordered_recurse(node, prev_solution):

            solution = list(prev_solution) + [node.value]

            # if the node does not fulfill constraints, this is a dead end.
            # constraints are applied in order; we bail on first false result.
            valid = True
            for constraint in constraints:
                if not constraint(solution):
                    valid = False
                    break

            if valid:
                # else, if we find a complete solution, yield it
                if len(solution) == domain_length:
                    yield solution

                # and if we find an incomplete solution,
                # create child nodes, and recurse into them.
                else:
                    for x in domain[len(solution)]:
                        child = Node(x, parent=node, children=[])
                        node.append(child)
                        for y in ordered_recurse(child, solution):
                            yield y

        # randomized traversal
        if self.randomized:
            graphs = [Node(x) for x in domain[0]]
            while graphs:
                result = random_recurse(random.choice(graphs), [])
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
                for y in ordered_recurse(node, []):
                    yield y
