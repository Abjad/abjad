from abjad import *


def test_iterationtools_iterate_contexts_in_expr_01():

    staff = Staff([Voice("c'8 d'8"), Voice("e'8 f'8 g'8")])
    tuplet = Tuplet(Fraction(2, 3), staff[1][:])
    staff.is_parallel = True

    contexts = iterationtools.iterate_contexts_in_expr(staff)
    contexts = list(contexts)

    assert contexts[0] is staff
    assert contexts[1] is staff[0]
    assert contexts[2] is staff[1]

def test_iterationtools_iterate_contexts_in_expr_02():

    staff = Staff([Voice("c'8 d'8"), Voice("e'8 f'8 g'8")])
    tuplet = Tuplet(Fraction(2, 3), staff[1][:])
    staff.is_parallel = True

    contexts = iterationtools.iterate_contexts_in_expr(staff, reverse=True)
    contexts = list(contexts)

    assert contexts[0] is staff
    assert contexts[1] is staff[1]
    assert contexts[2] is staff[0]
