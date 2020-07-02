import abjad


def test_Selection__get_component_01():

    staff = abjad.Staff(
        r"""
        c'16
        r16
        d'8
        r8
        e'8.
        r8.
        f'4
        r4
        """
    )

    notes = [staff[0], staff[2], staff[4], staff[6]]
    rests = [staff[1], staff[3], staff[5], staff[7]]

    assert abjad.select(staff)._get_component(abjad.Note, 0) is notes[0]
    assert abjad.select(staff)._get_component(abjad.Note, 1) is notes[1]
    assert abjad.select(staff)._get_component(abjad.Note, 2) is notes[2]
    assert abjad.select(staff)._get_component(abjad.Note, 3) is notes[3]

    assert abjad.select(staff)._get_component(abjad.Rest, 0) is rests[0]
    assert abjad.select(staff)._get_component(abjad.Rest, 1) is rests[1]
    assert abjad.select(staff)._get_component(abjad.Rest, 2) is rests[2]
    assert abjad.select(staff)._get_component(abjad.Rest, 3) is rests[3]

    assert abjad.select(staff)._get_component(abjad.Staff, 0) is staff


def test_Selection__get_component_02():
    """
    Iterates backwards with negative values of n.
    """

    staff = abjad.Staff(
        r"""
        c'16
        r16
        d'8
        r8
        e'8.
        r8.
        f'4
        r4
        """
    )

    notes = [staff[0], staff[2], staff[4], staff[6]]
    rests = [staff[1], staff[3], staff[5], staff[7]]

    assert abjad.select(staff)._get_component(abjad.Note, -1) is notes[3]
    assert abjad.select(staff)._get_component(abjad.Note, -2) is notes[2]
    assert abjad.select(staff)._get_component(abjad.Note, -3) is notes[1]
    assert abjad.select(staff)._get_component(abjad.Note, -4) is notes[0]

    assert abjad.select(staff)._get_component(abjad.Rest, -1) is rests[3]
    assert abjad.select(staff)._get_component(abjad.Rest, -2) is rests[2]
    assert abjad.select(staff)._get_component(abjad.Rest, -3) is rests[1]
    assert abjad.select(staff)._get_component(abjad.Rest, -4) is rests[0]
