from abjad import *


def test_componenttools__get_nth_component_in_time_order_from_01():

    staff = Staff(r"c'4 \times 2/3 { d'8 e'8 f'8 } g'2")

    assert testtools.compare(
        staff,
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

    leaves = staff.select_leaves()
    tuplet = staff[1]

    assert componenttools.get_nth_component_in_time_order_from_component(
        leaves[0], -1) is None
    assert componenttools.get_nth_component_in_time_order_from_component(
        leaves[0], 0) is leaves[0]
    assert componenttools.get_nth_component_in_time_order_from_component(
        leaves[0], 1) is tuplet
    assert componenttools.get_nth_component_in_time_order_from_component(
        leaves[0], 2) is leaves[4]
    assert componenttools.get_nth_component_in_time_order_from_component(
        leaves[0], 3) is None

    assert componenttools.get_nth_component_in_time_order_from_component(
        tuplet, -2) is None
    assert componenttools.get_nth_component_in_time_order_from_component(
        tuplet, -1) is leaves[0]
    assert componenttools.get_nth_component_in_time_order_from_component(
        tuplet, 0) is tuplet
    assert componenttools.get_nth_component_in_time_order_from_component(
        tuplet, 1) is leaves[4]

    assert componenttools.get_nth_component_in_time_order_from_component(
        leaves[1], -1) is leaves[0]
    assert componenttools.get_nth_component_in_time_order_from_component(
        leaves[1], 0) is leaves[1]
    assert componenttools.get_nth_component_in_time_order_from_component(
        leaves[1], 1) is leaves[2]
    assert componenttools.get_nth_component_in_time_order_from_component(
        leaves[1], 2) is leaves[3]
    assert componenttools.get_nth_component_in_time_order_from_component(
        leaves[1], 3) is leaves[4]
    assert componenttools.get_nth_component_in_time_order_from_component(
        leaves[1], 4) is None
