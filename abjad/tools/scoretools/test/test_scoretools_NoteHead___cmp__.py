import abjad


def test_scoretools_NoteHead___cmp___01():

    note_head_1 = abjad.NoteHead(12)
    note_head_2 = abjad.NoteHead(12)

    assert not note_head_1 <  note_head_2
    assert      note_head_1 <= note_head_2
    assert      note_head_1 == note_head_2
    assert not note_head_1 != note_head_2
    assert not note_head_1 >  note_head_2
    assert      note_head_1 >= note_head_2


def test_scoretools_NoteHead___cmp___02():

    note_head_1 = abjad.NoteHead(12)
    note_head_2 = abjad.NoteHead(13)

    assert not note_head_2 <  note_head_1
    assert not note_head_2 <= note_head_1
    assert not note_head_2 == note_head_1
    assert      note_head_2 != note_head_1
    assert      note_head_2 >  note_head_1
    assert      note_head_2 >= note_head_1


def test_scoretools_NoteHead___cmp___03():

    note_head_1 = abjad.NoteHead(12)
    note_head_2 = 12

    assert not note_head_1 <  note_head_2
    assert      note_head_1 <= note_head_2
    assert      note_head_1 == note_head_2
    assert not note_head_1 != note_head_2
    assert not note_head_1 >  note_head_2
    assert      note_head_1 >= note_head_2


def test_scoretools_NoteHead___cmp___04():

    note_head_1 = abjad.NoteHead(12)
    note_head_2 = 13

    assert not note_head_2 <  note_head_1
    assert not note_head_2 <= note_head_1
    assert not note_head_2 == note_head_1
    assert      note_head_2 != note_head_1
    assert      note_head_2 >  note_head_1
    assert      note_head_2 >= note_head_1
