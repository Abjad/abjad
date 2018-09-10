import abjad


def test_Mutation_replace_01():
    """
    Moves parentage and spanners from two old notes to five new notes.

    Equivalent to staff[1:3] = new_notes.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.beam(staff[:2])
    abjad.beam(staff[2:])
    abjad.hairpin('< !', staff[:])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            \<
            [
            d'8
            ]
            e'8
            [
            f'8
            \!
            ]
        }
        """
        ), print(format(staff))

    old_notes = staff[1:3]
    new_notes = 5 * abjad.Note("c''16")
    abjad.mutate(old_notes).replace(new_notes)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            \<
            [
            c''16
            c''16
            c''16
            c''16
            c''16
            f'8
            \!
            ]
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Mutation_replace_02():
    """
    Moves parentage and spanners from one old note to five new notes.

    Equivalent to staff[:1] = new_notes.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.beam(staff[:2])
    abjad.beam(staff[2:])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'8
            ]
            e'8
            [
            f'8
            ]
        }
        """
        ), print(format(staff))

    old_notes = staff[:1]
    new_notes = 5 * abjad.Note("c''16")
    abjad.mutate(old_notes).replace(new_notes)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c''16
            c''16
            c''16
            c''16
            c''16
            d'8
            ]
            e'8
            [
            f'8
            ]
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Mutation_replace_03():
    """
    Moves parentage and spanners from two old notes to five new notes.

    Equivalent to staff[:2] = new_notes.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.beam(staff[:2])
    abjad.beam(staff[2:])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'8
            ]
            e'8
            [
            f'8
            ]
        }
        """
        ), print(format(staff))

    old_notes = staff[:2]
    new_notes = 5 * abjad.Note("c''16")
    abjad.mutate(old_notes).replace(new_notes)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c''16
            c''16
            c''16
            c''16
            c''16
            e'8
            [
            f'8
            ]
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Mutation_replace_04():
    """
    Moves parentage and spanners from three old notes to five new notes.

    "Equivalent to staff[:3] = new_notes."
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.beam(staff[:2])
    abjad.beam(staff[2:])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'8
            ]
            e'8
            [
            f'8
            ]
        }
        """
        ), print(format(staff))

    old_notes = staff[:3]
    new_notes = 5 * abjad.Note("c''16")
    abjad.mutate(old_notes).replace(new_notes)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c''16
            c''16
            c''16
            c''16
            c''16
            f'8
            ]
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Mutation_replace_05():
    """
    Moves parentage and spanners from four old notes to five new notes.

    Equivalent to staff[:] = new_notes.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.beam(staff[:2])
    abjad.beam(staff[2:])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'8
            ]
            e'8
            [
            f'8
            ]
        }
        """
        ), print(format(staff))

    old_notes = staff[:]
    new_notes = 5 * abjad.Note("c''16")
    abjad.mutate(old_notes).replace(new_notes)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c''16
            c''16
            c''16
            c''16
            c''16
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Mutation_replace_06():
    """
    Moves parentage and spanners from container to children of container.

    Replaces container with contents of container.

    Effectively removes container from score.

    Equivalent to staff[:1] = staff[0][:].
    """

    staff = abjad.Staff([abjad.Voice("c'8 d'8 e'8 f'8")])
    abjad.beam(staff[0][:])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                c'8
                [
                d'8
                e'8
                f'8
                ]
            }
        }
        """
        ), print(format(staff))

    voice_selection = staff[:1]
    voice = voice_selection[0]
    old_components = abjad.mutate(voice_selection).replace(staff[0][:])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'8
            e'8
            f'8
            ]
        }
        """
        ), print(format(staff))

    assert not voice
    assert abjad.inspect(staff).wellformed()
