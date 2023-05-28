import copy

import pytest

import abjad


def test_Staff___copy___01():
    """
    Staves (shallow) copy grob overrides and context settings but not
    components.
    """

    staff_1 = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff_1).NoteHead.color = "#red"
    abjad.setting(staff_1).tupletFullLength = True

    staff_2 = copy.copy(staff_1)

    assert abjad.lilypond(staff_2) == abjad.string.normalize(
        r"""
        \new Staff
        \with
        {
            \override NoteHead.color = #red
            tupletFullLength = ##t
        }
        {
        }
        """
    )


def test_Staff___delitem___01():
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
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    assert isinstance(staff[4], abjad.Tuplet)
    del staff[0]
    assert len(staff) == 4
    assert isinstance(staff[0], abjad.Rest)
    assert isinstance(staff[1], abjad.Chord)
    assert isinstance(staff[2], abjad.Skip)
    assert isinstance(staff[3], abjad.Tuplet)
    del staff[0]
    assert len(staff) == 3
    assert isinstance(staff[0], abjad.Chord)
    assert isinstance(staff[1], abjad.Skip)
    assert isinstance(staff[2], abjad.Tuplet)
    del staff[0]
    assert len(staff) == 2
    assert isinstance(staff[0], abjad.Skip)
    assert isinstance(staff[1], abjad.Tuplet)
    del staff[0]
    assert len(staff) == 1
    assert isinstance(staff[0], abjad.Tuplet)
    del staff[0]
    assert len(staff) == 0


def test_Staff___delitem___02():
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
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    assert isinstance(staff[4], abjad.Tuplet)
    del staff[-1]
    assert len(staff) == 4
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    del staff[-1]
    assert len(staff) == 3
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    del staff[-1]
    assert len(staff) == 2
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    del staff[-1]
    assert len(staff) == 1
    assert isinstance(staff[0], abjad.Note)
    del staff[-1]
    assert len(staff) == 0


def test_Staff___delitem___03():
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
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    assert isinstance(staff[4], abjad.Tuplet)
    del staff[3]
    assert len(staff) == 4
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Tuplet)
    del staff[-2]
    assert len(staff) == 3
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Tuplet)
    del staff[2]
    assert len(staff) == 2
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    del staff[0]
    assert len(staff) == 1
    assert isinstance(staff[0], abjad.Rest)
    del staff[-1]
    assert len(staff) == 0


def test_Staff___getitem___01():
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
    assert isinstance(staff[-5], abjad.Note)
    assert isinstance(staff[-4], abjad.Rest)
    assert isinstance(staff[-3], abjad.Chord)
    assert isinstance(staff[-2], abjad.Skip)
    assert isinstance(staff[-1], abjad.Tuplet)


def test_Staff___getitem___02():
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
    components = staff[0:0]
    assert len(components) == 0
    assert abjad.wf.wellformed(staff)


def test_Staff___getitem___03():
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
    components = staff[0:1]
    assert len(components) == 1
    assert isinstance(components[0], abjad.Note)
    for x in staff:
        assert x._parent == staff
    assert abjad.wf.wellformed(staff)


def test_Staff___getitem___04():
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
    components = staff[-1:]
    assert len(components) == 1
    assert isinstance(components[0], abjad.Tuplet)
    for x in components:
        assert x._parent == staff
    assert abjad.wf.wellformed(staff)


def test_Staff___getitem___05():
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
    components = staff[1:-1]
    assert len(components) == 3
    assert isinstance(components[0], abjad.Rest)
    assert isinstance(components[1], abjad.Chord)
    assert isinstance(components[2], abjad.Skip)
    for x in components:
        assert x._parent == staff
    assert abjad.wf.wellformed(staff)


def test_Staff___getitem___06():
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
    components = staff[2:]
    assert len(components) == 3
    assert isinstance(components[0], abjad.Chord)
    assert isinstance(components[1], abjad.Skip)
    assert isinstance(components[2], abjad.Tuplet)
    for x in components:
        assert x._parent == staff
    assert abjad.wf.wellformed(staff)


def test_Staff___getitem___07():
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
    components = staff[:-2]
    assert len(components) == 3
    assert isinstance(components[0], abjad.Note)
    assert isinstance(components[1], abjad.Rest)
    assert isinstance(components[2], abjad.Chord)
    for x in components:
        assert x._parent == staff
    assert abjad.wf.wellformed(staff)


def test_Staff___getitem___08():
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
    components = staff[:]
    assert len(components) == 5
    assert isinstance(components[0], abjad.Note)
    assert isinstance(components[1], abjad.Rest)
    assert isinstance(components[2], abjad.Chord)
    assert isinstance(components[3], abjad.Skip)
    assert isinstance(components[4], abjad.Tuplet)
    assert all(_._parent is staff for _ in staff)


def test_Staff___init___01():
    """
    Initialize with context name.
    """

    staff = abjad.Staff(lilypond_type="BlueStaff")
    assert staff.lilypond_type == "BlueStaff"


def test_Staff___init___02():
    """
    Initialize with name.
    """

    staff = abjad.Staff(name="FirstBlueStaff")
    assert staff.name == "FirstBlueStaff"


def test_Staff___init___03():
    """
    Initialize with both context name and name.
    """

    staff = abjad.Staff(lilypond_type="BlueStaff", name="FirstBlueStaff")
    assert staff.lilypond_type == "BlueStaff"
    assert staff.name == "FirstBlueStaff"


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
        assert x.written_pitch == "d'"
    for x in staff[4:8]:
        assert x.written_pitch == "c'"
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


def test_Staff_append_01():
    """
    Append one note.
    """

    staff = abjad.Staff("c'4 c'4 c'4 c'4")
    staff.append(abjad.Note("c'4"))
    assert abjad.wf.wellformed(staff)
    assert len(staff) == 5
    assert staff._get_contents_duration() == abjad.Duration(5, 4)


def test_Staff_append_02():
    """
    Append one chord.
    """

    staff = abjad.Staff("c'4 c'4 c'4 c'4")
    staff.append(abjad.Chord([2, 3, 4], (1, 4)))
    assert abjad.wf.wellformed(staff)
    assert len(staff) == 5
    assert staff._get_contents_duration() == abjad.Duration(5, 4)


def test_Staff_append_03():
    """
    Append one tuplet.
    """

    staff = abjad.Staff("c'4 c'4 c'4 c'4")
    staff.append(abjad.Tuplet((2, 3), "c'8 c'8 c'8"))
    assert abjad.wf.wellformed(staff)
    assert len(staff) == 5
    assert staff._get_contents_duration() == abjad.Duration(5, 4)


def test_Staff_engraver_consists_01():
    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    staff.consists_commands.append("Horizontal_bracket_engraver")
    staff.consists_commands.append("Instrument_name_engraver")

    assert abjad.wf.wellformed(staff)
    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        \with
        {
            \consists Horizontal_bracket_engraver
            \consists Instrument_name_engraver
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )


def test_Staff_engraver_removals_01():
    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    staff.remove_commands.append("Time_signature_engraver")
    staff.remove_commands.append("Bar_number_engraver")

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        \with
        {
            \remove Time_signature_engraver
            \remove Bar_number_engraver
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    assert abjad.wf.wellformed(staff)
