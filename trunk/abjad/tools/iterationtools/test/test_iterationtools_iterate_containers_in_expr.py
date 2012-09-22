from abjad import *


def test_iterationtools_iterate_containers_in_expr_01():

    staff = Staff([Voice("c'8 d'8"), Voice("e'8 f'8 g'8")])
    tuplet = Tuplet(Fraction(2, 3), staff[1][:])
    staff.is_parallel = True

    containers = iterationtools.iterate_containers_in_expr(staff, reverse=True)
    containers = list(containers)

    assert containers[0] is staff
    assert containers[1] is staff[1]
    assert containers[2] is tuplet
    assert containers[3] is staff[0]

def test_iterationtools_iterate_containers_in_expr_02():

    staff = Staff([Voice("c'8 d'8"), Voice("e'8 f'8 g'8")])
    tuplet = Tuplet(Fraction(2, 3), staff[1][:])
    staff.is_parallel = True

    containers = iterationtools.iterate_containers_in_expr(staff)
    containers = list(containers)

    assert containers[0] is staff
    assert containers[1] is staff[0]
    assert containers[2] is staff[1]
    assert containers[3] is tuplet
