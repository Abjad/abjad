from abjad import *


def test_resttools_iterate_rests_forward_in_expr_01():

    staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")

    rests = resttools.iterate_rests_forward_in_expr(staff)
    rests = list(rests)

    assert rests[0] is staff[2]
    assert rests[1] is staff[4]
