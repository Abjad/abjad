import abjad


def test_Mutation_extract_01():
    """
    Extracts note.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    abjad.glissando(voice[:])

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \glissando %! abjad.glissando(7)
            d'8
            \glissando %! abjad.glissando(7)
            e'8
            \glissando %! abjad.glissando(7)
            f'8
            ]
        }
        """
    ), print(format(voice))

    note = voice[1]
    abjad.mutate(note).extract()

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \glissando %! abjad.glissando(7)
            e'8
            \glissando %! abjad.glissando(7)
            f'8
            ]
        }
        """
    ), print(format(voice))

    assert abjad.inspect(note).wellformed()
    assert abjad.inspect(voice).wellformed()


def test_Mutation_extract_02():
    """
    Extracts multiple notes.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    abjad.glissando(voice[:])

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \glissando %! abjad.glissando(7)
            d'8
            \glissando %! abjad.glissando(7)
            e'8
            \glissando %! abjad.glissando(7)
            f'8
            ]
        }
        """
    ), print(format(voice))

    notes = voice[:2]
    for note in notes:
        abjad.mutate(note).extract()

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            e'8
            \glissando %! abjad.glissando(7)
            f'8
            ]
        }
        """
    ), print(format(voice))

    for note in notes:
        assert abjad.inspect(note).wellformed()

    assert abjad.inspect(voice).wellformed()


def test_Mutation_extract_03():
    """
    Extracts container.
    """

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8"))
    staff.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'8
                [
                d'8
            }
            {
                e'8
                f'8
                ]
            }
        }
        """
    ), print(format(staff))

    container = staff[0]
    abjad.mutate(container).extract()

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'8
            {
                e'8
                f'8
                ]
            }
        }
        """
    ), print(format(staff))

    assert not container
    assert abjad.inspect(staff).wellformed()


def test_Mutation_extract_04():
    """
    Extracts multiple containers.
    """

    voice = abjad.Voice()
    voice.append(abjad.Container("c'8 d'8"))
    voice.append(abjad.Container("e'8 f'8"))
    voice.append(abjad.Container("g'8 a'8"))
    leaves = abjad.select(voice).leaves()
    abjad.beam(leaves)
    abjad.glissando(leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                \glissando %! abjad.glissando(7)
                d'8
                \glissando %! abjad.glissando(7)
            }
            {
                e'8
                \glissando %! abjad.glissando(7)
                f'8
                \glissando %! abjad.glissando(7)
            }
            {
                g'8
                \glissando %! abjad.glissando(7)
                a'8
                ]
            }
        }
        """
    ), print(format(voice))

    containers = voice[:2]
    for container in containers:
        abjad.mutate(container).extract()

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \glissando %! abjad.glissando(7)
            d'8
            \glissando %! abjad.glissando(7)
            e'8
            \glissando %! abjad.glissando(7)
            f'8
            \glissando %! abjad.glissando(7)
            {
                g'8
                \glissando %! abjad.glissando(7)
                a'8
                ]
            }
        }
        """
    ), print(format(voice))

    for container in containers:
        assert not container

    assert abjad.inspect(voice).wellformed()
