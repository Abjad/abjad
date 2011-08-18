from abjad import *


def test_resttools_yield_groups_of_rests_in_sequence_01():

    staff = Staff("c'8 d'8 r8 r8 <e' g'>8 <f' a'>8 g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")
    rest_groups = resttools.yield_groups_of_rests_in_sequence(staff)
    rest_groups = list(rest_groups)

    assert rest_groups[0] == (staff[2], staff[3])
    assert rest_groups[1] == (staff[8], staff[9])
