from abjad import *


def test_chordtools_yield_groups_of_chords_in_sequence_01():

    staff = Staff("c'8 d'8 r8 r8 <e' g'>8 <f' a'>8 g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")
    chord_groups = chordtools.yield_groups_of_chords_in_sequence(staff)
    chord_groups = list(chord_groups)

    assert chord_groups[0] == (staff[4], staff[5])
    assert chord_groups[1] == (staff[10], staff[11])
