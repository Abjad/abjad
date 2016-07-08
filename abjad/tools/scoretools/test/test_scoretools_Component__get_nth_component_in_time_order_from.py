from abjad import *


def test_scoretools_Component__get_nth_component_in_time_order_from_01():

    staff = Staff(r"c'4 \times 2/3 { d'8 e'8 f'8 } g'2")

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'4
            \times 2/3 {
                d'8
                e'8
                f'8
            }
            g'2
        }
        '''
        )

    leaves = select(staff).by_leaf()
    tuplet = staff[1]

    assert leaves[0]._get_nth_component_in_time_order_from(-1) is None
    assert leaves[0]._get_nth_component_in_time_order_from(0) is leaves[0]
    assert leaves[0]._get_nth_component_in_time_order_from(1) is tuplet
    assert leaves[0]._get_nth_component_in_time_order_from(2) is leaves[4]
    assert leaves[0]._get_nth_component_in_time_order_from(3) is None

    assert tuplet._get_nth_component_in_time_order_from(-2) is None
    assert tuplet._get_nth_component_in_time_order_from(-1) is leaves[0]
    assert tuplet._get_nth_component_in_time_order_from(0) is tuplet
    assert tuplet._get_nth_component_in_time_order_from(1) is leaves[4]

    assert leaves[1]._get_nth_component_in_time_order_from(-1) is leaves[0]
    assert leaves[1]._get_nth_component_in_time_order_from(0) is leaves[1]
    assert leaves[1]._get_nth_component_in_time_order_from(1) is leaves[2]
    assert leaves[1]._get_nth_component_in_time_order_from(2) is leaves[3]
    assert leaves[1]._get_nth_component_in_time_order_from(3) is leaves[4]
    assert leaves[1]._get_nth_component_in_time_order_from(4) is None
