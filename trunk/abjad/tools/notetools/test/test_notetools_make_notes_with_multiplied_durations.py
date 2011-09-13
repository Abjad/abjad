from abjad import *


def test_notetools_make_notes_with_multiplied_durations_01():

    notes = notetools.make_notes_with_multiplied_durations(
        0, Duration(1, 4), [(1, 2), (1, 3), (1, 4), (1, 5)])
    staff = Staff(notes)

    assert staff.format == "\\new Staff {\n\tc'4 * 2\n\tc'4 * 4/3\n\tc'4 * 1\n\tc'4 * 4/5\n}"
