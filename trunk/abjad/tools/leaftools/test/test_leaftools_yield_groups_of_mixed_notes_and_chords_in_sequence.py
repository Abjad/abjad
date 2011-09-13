from abjad import *


def test_leaftools_yield_groups_of_mixed_notes_and_chords_in_sequence_01():

    staff = Staff("c'8 d'8 r8 r8 <e' g'>8 <f' a'>8 g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")
    groups = leaftools.yield_groups_of_mixed_notes_and_chords_in_sequence(staff)
    groups = list(groups)

    assert groups[0] == (staff[0], staff[1])
    assert groups[1] == (staff[4], staff[5], staff[6], staff[7])
    assert groups[2] == (staff[10], staff[11])
