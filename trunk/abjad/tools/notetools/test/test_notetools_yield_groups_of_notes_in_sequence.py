from abjad import *


def test_notetools_yield_groups_of_notes_in_sequence_01():

    staff = Staff("c'8 d'8 r8 r8 <e' g'>8 <f' a'>8 g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")
    note_groups = notetools.yield_groups_of_notes_in_sequence(staff)
    note_groups = list(note_groups)

    assert note_groups[0] == (staff[0], staff[1])
    assert note_groups[1] == (staff[6], staff[7])
