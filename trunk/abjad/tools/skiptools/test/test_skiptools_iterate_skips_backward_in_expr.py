from abjad import *


def test_skiptools_iterate_skips_backward_in_expr_01():

    staff = Staff("<e' g' c''>8 a'8 s8 <d' f' b'>8 s2")

    skips = skiptools.iterate_skips_backward_in_expr(staff)
    skips = list(skips)

    assert skips[0] is staff[4]
    assert skips[1] is staff[2]
