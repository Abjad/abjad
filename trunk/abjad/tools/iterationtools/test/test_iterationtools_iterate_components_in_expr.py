from abjad import *


def test_iterationtools_iterate_components_in_expr_01():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam = spannertools.BeamSpanner(staff[:])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [
                d'8
            }
            {
                e'8
                f'8 ]
            }
        }
        '''
        )

    components = iterationtools.iterate_components_in_expr(beam, reverse=True)
    components = list(components)
    leaves = staff.select_leaves()

    assert components[0] is staff[-1]
    assert components[1] is leaves[-1]
    assert components[2] is leaves[-2]
    assert components[3] is staff[-2]
    assert components[4] is leaves[-3]
    assert components[5] is leaves[-4]


def test_iterationtools_iterate_components_in_expr_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    spanner = spannertools.BeamSpanner(staff[2:])

    notes = iterationtools.iterate_components_in_expr(spanner)
    assert list(notes) == staff[2:]
