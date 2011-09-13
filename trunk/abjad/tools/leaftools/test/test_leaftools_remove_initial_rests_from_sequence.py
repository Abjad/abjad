from abjad import *


def test_leaftools_remove_initial_rests_from_sequence_01():

    staff = Staff("r8 r8 e'8 f'8 r4 r4")
    leaves = leaftools.remove_initial_rests_from_sequence(staff)

    assert leaves == list(staff.leaves[2:])
