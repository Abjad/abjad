from experimental.tools.constrainttools import *


def test_FixedLengthStreamSolver_01():
    domain = Domain([1, 2, 3, 4], 4)
    all_unique = GlobalCountsConstraint(lambda x: all([y == 1 for y in x.values()]))
    max_interval = RelativeIndexConstraint([0, 1], lambda x, y: abs(x - y) < 3)

    ordered_solver = FixedLengthStreamSolver(domain, [all_unique, max_interval])

    ordered_solutions = [x for x in ordered_solver]
    assert ordered_solutions == [
        [1, 2, 3, 4],
        [1, 2, 4, 3],
        [1, 3, 2, 4],
        [1, 3, 4, 2],
        [2, 1, 3, 4],
        [2, 4, 3, 1],
        [3, 1, 2, 4],
        [3, 4, 2, 1],
        [4, 2, 1, 3],
        [4, 2, 3, 1],
        [4, 3, 1, 2],
        [4, 3, 2, 1],
    ]

    random_solver = FixedLengthStreamSolver(domain, [all_unique, max_interval], randomized=True)
    random_solutions = [x for x in random_solver]

    assert list(sorted(random_solutions)) == ordered_solutions
    
    more_random_solutions = [x for x in random_solver]

    assert list(sorted(random_solutions)) == list(sorted(more_random_solutions))
    assert random_solutions != more_random_solutions
