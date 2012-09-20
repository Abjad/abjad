from abjad import *


def test_iterationtools_iterate_leaves_in_expr_01():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    r'''
    \new Staff {
      {
            \time 2/8
            c'8
            d'8
      }
      {
            \time 2/8
            e'8
            f'8
      }
      {
            \time 2/8
            g'8
            a'8
      }
    }
    '''

    generator = iterationtools.iterate_leaves_in_expr(staff, reverse=True)
    leaves = list(generator)

    assert leaves[0] is staff[2][1]
    assert leaves[1] is staff[2][0]
    assert leaves[2] is staff[1][1]
    assert leaves[3] is staff[1][0]
    assert leaves[4] is staff[0][1]
    assert leaves[5] is staff[0][0]


def test_iterationtools_iterate_leaves_in_expr_02():
    '''Optional start and stop keyword parameters.'''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    leaves = list(iterationtools.iterate_leaves_in_expr(staff, start=3, reverse=True))
    assert leaves[0] is staff[1][0]
    assert leaves[1] is staff[0][1]
    assert leaves[2] is staff[0][0]
    assert len(leaves) == 3

    leaves = list(iterationtools.iterate_leaves_in_expr(staff, start=0, stop=3, reverse=True))
    assert leaves[0] is staff[2][1]
    assert leaves[1] is staff[2][0]
    assert leaves[2] is staff[1][1]
    assert len(leaves) == 3

    leaves = list(iterationtools.iterate_leaves_in_expr(staff, start=2, stop=4, reverse=True))
    assert leaves[0] is staff[1][1]
    assert leaves[1] is staff[1][0]
    assert len(leaves) == 2


def test_iterationtools_iterate_leaves_in_expr_03():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    r'''
    \new Staff {
      {
            \time 2/8
            c'8
            d'8
      }
      {
            \time 2/8
            e'8
            f'8
      }
      {
            \time 2/8
            g'8
            a'8
      }
    }
    '''

    generator = iterationtools.iterate_leaves_in_expr(staff)
    leaves = list(generator)

    assert leaves[0] is staff[0][0]
    assert leaves[1] is staff[0][1]
    assert leaves[2] is staff[1][0]
    assert leaves[3] is staff[1][1]
    assert leaves[4] is staff[2][0]
    assert leaves[5] is staff[2][1]


def test_iterationtools_iterate_leaves_in_expr_04():
    '''Optional start and stop keyword parameters.'''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    leaves = list(iterationtools.iterate_leaves_in_expr(staff, start=3))
    assert leaves[0] is staff[1][1]
    assert leaves[1] is staff[2][0]
    assert leaves[2] is staff[2][1]
    assert len(leaves) == 3

    leaves = list(iterationtools.iterate_leaves_in_expr(staff, start=0, stop=3))
    assert leaves[0] is staff[0][0]
    assert leaves[1] is staff[0][1]
    assert leaves[2] is staff[1][0]
    assert len(leaves) == 3

    leaves = list(iterationtools.iterate_leaves_in_expr(staff, start=2, stop=4))
    assert leaves[0] is staff[1][0]
    assert leaves[1] is staff[1][1]
    assert len(leaves) == 2
