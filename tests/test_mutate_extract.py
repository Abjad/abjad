import abjad


def test_mutate_extract_01():
    """
    Extracts note.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    abjad.glissando(voice[:])

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    ), print(abjad.lilypond(voice))

    note = voice[1]
    abjad.mutate.extract(note)

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(note)
    assert abjad.wf.wellformed(voice)


def test_mutate_extract_02():
    """
    Extracts multiple notes.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    abjad.glissando(voice[:])

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    ), print(abjad.lilypond(voice))

    notes = voice[:2]
    for note in notes:
        abjad.mutate.extract(note)

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            e'8
            \glissando %! abjad.glissando(7)
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(voice))

    for note in notes:
        assert abjad.wf.wellformed(note)

    assert abjad.wf.wellformed(voice)


def test_mutate_extract_03():
    """
    Extracts container.
    """

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8"))
    staff.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    container = staff[0]
    abjad.mutate.extract(container)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    assert not container
    assert abjad.wf.wellformed(staff)


def test_mutate_extract_04():
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

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    ), print(abjad.lilypond(voice))

    containers = voice[:2]
    for container in containers:
        abjad.mutate.extract(container)

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    ), print(abjad.lilypond(voice))

    for container in containers:
        assert not container

    assert abjad.wf.wellformed(voice)
