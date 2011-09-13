from abjad import *


def test_notetools_make_repeated_notes_from_time_signature_01():
    '''Make repeated notes from integer pair.
    '''

    notes = notetools.make_repeated_notes_from_time_signature((5, 32), pitch = "d''")
    staff = Staff(notes)

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\td''32\n\td''32\n\td''32\n\td''32\n\td''32\n}"


def test_notetools_make_repeated_notes_from_time_signature_02():
    '''Make repeated notes from time signature.
    '''

    time_signature = contexttools.TimeSignatureMark((5, 32))
    notes = notetools.make_repeated_notes_from_time_signature(time_signature, pitch = "d''")
    staff = Staff(notes)

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\td''32\n\td''32\n\td''32\n\td''32\n\td''32\n}"
