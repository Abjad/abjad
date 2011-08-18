from abjad import *


def test_containertools_iterate_containers_forward_in_expr_01():

    staff = Staff([Voice("c'8 d'8"), Voice("e'8 f'8 g'8")])
    tuplet = Tuplet(Fraction(2, 3), staff[1][:])
    staff.is_parallel = True

    containers = containertools.iterate_containers_forward_in_expr(staff)
    containers = list(containers)

    assert containers[0] is staff
    assert containers[1] is staff[0]
    assert containers[2] is staff[1]
    assert containers[3] is tuplet
