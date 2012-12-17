from experimental.tools.constrainttools import *


def test_VariableLengthStreamSolver_01():
    domain = Domain([1, 2, 3, 4], 1)
    boundary_sum = GlobalConstraint(lambda x: sum(x) < 6)
    target_sum = GlobalConstraint(lambda x: sum(x) == 5)

    ordered_solver = VariableLengthStreamSolver(domain, [boundary_sum], [target_sum], randomized=False)

    ordered_solutions = [x for x in ordered_solver]
    assert ordered_solutions == [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 2],
        [1, 1, 2, 1],
        [1, 1, 3],
        [1, 2, 1, 1],
        [1, 2, 2],
        [1, 3, 1],
        [1, 4],
        [2, 1, 1, 1],
        [2, 1, 2],
        [2, 2, 1],
        [2, 3],
        [3, 1, 1],
        [3, 2],
        [4, 1],
    ]

    random_solver = VariableLengthStreamSolver(domain, [boundary_sum], [target_sum], randomized=True)
    random_solutions = [x for x in random_solver]

    assert list(sorted(random_solutions)) == ordered_solutions
    
    more_random_solutions = [x for x in random_solver]

    assert list(sorted(random_solutions)) == list(sorted(more_random_solutions))
    assert random_solutions != more_random_solutions
