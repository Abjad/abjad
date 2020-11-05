import pytest

import abjad


def test_Staff___setitem___01():

    staff = abjad.Staff(
        [
            abjad.Note("c'4"),
            abjad.Rest((1, 4)),
            abjad.Chord([2, 3, 4], (1, 4)),
            abjad.Skip((1, 4)),
            abjad.Tuplet((4, 5), "c'16 c'16 c'16 c'16"),
        ]
    )

    assert len(staff) == 5
    assert abjad.wf.wellformed(staff)
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    assert isinstance(staff[4], abjad.Tuplet)
    staff[1] = abjad.Chord([12, 13, 15], (1, 4))
    assert len(staff) == 5
    assert abjad.wf.wellformed(staff)
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Chord)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    assert isinstance(staff[4], abjad.Tuplet)
    staff[0] = abjad.Rest((1, 4))
    assert len(staff) == 5
    assert abjad.wf.wellformed(staff)
    assert isinstance(staff[0], abjad.Rest)
    assert isinstance(staff[1], abjad.Chord)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    assert isinstance(staff[4], abjad.Tuplet)
    staff[-2] = abjad.Tuplet((2, 3), "c'8 c'8 c'8")
    assert len(staff) == 5
    assert abjad.wf.wellformed(staff)
    assert isinstance(staff[0], abjad.Rest)
    assert isinstance(staff[1], abjad.Chord)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Tuplet)
    assert isinstance(staff[4], abjad.Tuplet)
    staff[-1] = abjad.Note(13, (1, 4))
    assert len(staff) == 5
    assert abjad.wf.wellformed(staff)
    assert isinstance(staff[0], abjad.Rest)
    assert isinstance(staff[1], abjad.Chord)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Tuplet)
    assert isinstance(staff[4], abjad.Note)
    staff[-3] = abjad.Skip((1, 4))
    assert len(staff) == 5
    assert abjad.wf.wellformed(staff)
    assert isinstance(staff[0], abjad.Rest)
    assert isinstance(staff[1], abjad.Chord)
    assert isinstance(staff[2], abjad.Skip)
    assert isinstance(staff[3], abjad.Tuplet)
    assert isinstance(staff[4], abjad.Note)


def test_Staff___setitem___02():
    """
    Reassign the entire contents of staff.
    """

    staff = abjad.Staff("c'4 c'4 c'4 c'4")
    assert staff._get_contents_duration() == abjad.Duration(4, 4)
    staff[:] = "c'8 c'8 c'8 c'8"
    assert staff._get_contents_duration() == abjad.Duration(4, 8)


def test_Staff___setitem___03():
    """
    Item-assign an empty container to staff.
    """

    staff = abjad.Staff("c'4 c'4 c'4 c'4")
    staff[0] = abjad.Voice([])


def test_Staff___setitem___04():
    """
    Slice-assign empty containers to staff.
    """

    staff = abjad.Staff("c'4 c'4 c'4 c'4")
    staff[0:2] = [abjad.Voice([]), abjad.Voice([])]


def test_Staff___setitem___05():
    """
    Bark when user assigns a slice to an item.
    """

    staff = abjad.Staff("c'4 c'4 c'4 c'4")

    with pytest.raises(AssertionError):
        staff[0] = [abjad.Note(2, (1, 4)), abjad.Note(2, (1, 4))]


def test_Staff___setitem___06():
    """
    Bark when user assigns an item to a slice.
    """

    staff = abjad.Staff("c'4 c'4 c'4 c'4")

    with pytest.raises(Exception):
        staff[0:2] = abjad.Note(2, (1, 4))


def test_Staff___setitem___07():
    """
    Slice-assign notes.
    """

    staff = abjad.Staff("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")
    staff[0:4] = "d'8 d'8 d'8 d'8"
    assert len(staff) == 8
    for x in staff[0:4]:
        assert x.written_pitch == 2
    for x in staff[4:8]:
        assert x.written_pitch == 0
    assert abjad.wf.wellformed(staff)


def test_Staff___setitem___08():
    """
    Slice-assign chords.
    """

    staff = abjad.Staff("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")
    chord = abjad.Chord([2, 3, 4], (1, 4))
    chords = abjad.mutate.copy(chord, 4)
    staff[0:4] = chords
    assert len(staff) == 8
    for x in staff[0:4]:
        assert x.written_duration == abjad.Duration(1, 4)
    for x in staff[4:8]:
        assert x.written_duration == abjad.Duration(1, 8)
    assert abjad.wf.wellformed(staff)


def test_Staff___setitem___09():
    """
    Slice-assign tuplets.
    """

    staff = abjad.Staff("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")
    tuplet = abjad.Tuplet((2, 3), "c'8 c'8 c'8")
    tuplets = abjad.mutate.copy(tuplet, 2)
    staff[0:4] = tuplets
    assert len(staff) == 6
    for i, x in enumerate(staff):
        if i in [0, 1]:
            assert isinstance(x, abjad.Tuplet)
        else:
            assert isinstance(x, abjad.Note)
    assert abjad.wf.wellformed(staff)
