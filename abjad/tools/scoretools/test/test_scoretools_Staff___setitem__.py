import abjad
import pytest


def test_scoretools_Staff___setitem___01():

    staff = abjad.Staff([
        abjad.Note("c'4"),
        abjad.Rest((1, 4)),
        abjad.Chord([2, 3, 4], (1, 4)),
        abjad.Skip((1, 4)),
        abjad.Tuplet((4, 5), 4 * abjad.Note(0, (1, 16))),
        ])

    assert len(staff) == 5
    assert abjad.inspect(staff).is_well_formed()
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    assert isinstance(staff[4], abjad.Tuplet)
    staff[1] = abjad.Chord([12, 13, 15], (1, 4))
    assert len(staff) == 5
    assert abjad.inspect(staff).is_well_formed()
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Chord)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    assert isinstance(staff[4], abjad.Tuplet)
    staff[0] = abjad.Rest((1, 4))
    assert len(staff) == 5
    assert abjad.inspect(staff).is_well_formed()
    assert isinstance(staff[0], abjad.Rest)
    assert isinstance(staff[1], abjad.Chord)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    assert isinstance(staff[4], abjad.Tuplet)
    staff[-2] = abjad.Tuplet((2, 3), 3 * abjad.Note(0, (1, 8)))
    assert len(staff) == 5
    assert abjad.inspect(staff).is_well_formed()
    assert isinstance(staff[0], abjad.Rest)
    assert isinstance(staff[1], abjad.Chord)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Tuplet)
    assert isinstance(staff[4], abjad.Tuplet)
    staff[-1] = abjad.Note(13, (1, 4))
    assert len(staff) == 5
    assert abjad.inspect(staff).is_well_formed()
    assert isinstance(staff[0], abjad.Rest)
    assert isinstance(staff[1], abjad.Chord)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Tuplet)
    assert isinstance(staff[4], abjad.Note)
    staff[-3] = abjad.Skip((1, 4))
    assert len(staff) == 5
    assert abjad.inspect(staff).is_well_formed()
    assert isinstance(staff[0], abjad.Rest)
    assert isinstance(staff[1], abjad.Chord)
    assert isinstance(staff[2], abjad.Skip)
    assert isinstance(staff[3], abjad.Tuplet)
    assert isinstance(staff[4], abjad.Note)


def test_scoretools_Staff___setitem___02():
    r'''Reassign the entire contents of staff.
    '''

    staff = abjad.Staff(4 * abjad.Note("c'4"))
    assert staff._get_contents_duration() == abjad.Duration(4, 4)
    staff[:] = abjad.Note(0, (1, 8)) * 4
    assert staff._get_contents_duration() == abjad.Duration(4, 8)


def test_scoretools_Staff___setitem___03():
    r'''Item-assign an empty container to staff.
    '''

    staff = abjad.Staff(4 * abjad.Note("c'4"))
    staff[0] = abjad.Voice([])


def test_scoretools_Staff___setitem___04():
    r'''Slice-assign empty containers to staff.
    '''

    staff = abjad.Staff(4 * abjad.Note("c'4"))
    staff[0:2] = [abjad.Voice([]), abjad.Voice([])]


def test_scoretools_Staff___setitem___05():
    r'''Bark when user assigns a slice to an item.
    '''

    staff = abjad.Staff(4 * abjad.Note("c'4"))

    statement = 'staff[0] = [abjad.Note(2, (1, 4)), abjad.Note(2, (1, 4))]'
    assert pytest.raises(AssertionError, statement)


def test_scoretools_Staff___setitem___06():
    r'''Bark when user assigns an item to a slice.
    '''

    staff = abjad.Staff(4 * abjad.Note("c'4"))

    assert pytest.raises(Exception, 'staff[0:2] = abjad.Note(2, (1, 4))')


def test_scoretools_Staff___setitem___07():
    r'''Slice-assign notes.
    '''

    staff = abjad.Staff(abjad.Note(0, (1, 8)) * 8)
    staff[0:4] = abjad.Note(2, (1, 8)) * 4
    assert len(staff) == 8
    for x in staff[0:4]:
        assert x.written_pitch == 2
    for x in staff[4:8]:
        assert x.written_pitch == 0
    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Staff___setitem___08():
    r'''Slice-assign chords.
    '''

    staff = abjad.Staff(abjad.Note(0, (1, 8)) * 8)
    staff[0:4] = abjad.Chord([2, 3, 4], (1, 4)) * 4
    assert len(staff) == 8
    for x in staff[0:4]:
        assert x.written_duration == abjad.Duration(1, 4)
    for x in staff[4:8]:
        assert x.written_duration == abjad.Duration(1, 8)
    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Staff___setitem___09():
    r'''Slice-assign tuplets.
    '''

    staff = abjad.Staff(abjad.Note(0, (1, 8)) * 8)
    staff[0:4] = 2 * abjad.Tuplet((2, 3), 3 * abjad.Note(0, (1, 8)))
    assert len(staff) == 6
    for i, x in enumerate(staff):
        if i in [0, 1]:
            assert isinstance(x, abjad.Tuplet)
        else:
            assert isinstance(x, abjad.Note)
    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Staff___setitem___10():
    r'''Slice-assign measures.
    '''

    staff = abjad.Staff(abjad.Note(0, (1, 8)) * 8)
    staff[0:4] = abjad.Measure((2, 8), abjad.Note(0, (1, 8)) * 2) * 2
    assert len(staff) == 6
    for i, x in enumerate(staff):
        if i in [0, 1]:
            assert isinstance(x, abjad.Measure)
        else:
            assert isinstance(x, abjad.Note)
    assert abjad.inspect(staff).is_well_formed()
