from abjad import *


def test_skiptools_yield_groups_of_skips_in_sequence_01():

    staff = Staff("c'8 d'8 s8 s8 <e' g'>8 <f' a'>8 g'8 a'8 s8 s8 <b' d''>8 <c'' e''>8")
    skip_groups = skiptools.yield_groups_of_skips_in_sequence(staff)
    skip_groups = list(skip_groups)

    assert skip_groups[0] == (staff[2], staff[3])
    assert skip_groups[1] == (staff[8], staff[9])
