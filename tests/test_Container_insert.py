import abjad


def test_Container_insert_01():
    """
    Insert component into container at index i.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    voice.insert(0, abjad.Rest((1, 8)))

    assert abjad.wf.wellformed(voice)
    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            r8
            c'8
            [
            d'8
            e'8
            f'8
            ]
        }
        """
    )


def test_Container_insert_02():

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    voice.insert(1, abjad.Note(1, (1, 8)))

    assert abjad.wf.wellformed(voice)
    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            cs'8
            d'8
            e'8
            f'8
            ]
        }
        """
    )


def test_Container_insert_03():

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(4)])
    abjad.beam(staff[:])
    staff.insert(4, abjad.Rest((1, 4)))

    assert abjad.wf.wellformed(staff)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            cs'8
            d'8
            ef'8
            ]
            r4
        }
        """
    )


def test_Container_insert_04():
    """
    Insert works with really big positive values.
    """

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(4)])
    abjad.beam(staff[:])
    staff.insert(1000, abjad.Rest((1, 4)))

    assert abjad.wf.wellformed(staff)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            cs'8
            d'8
            ef'8
            ]
            r4
        }
        """
    )


def test_Container_insert_05():
    """
    Insert works with negative values.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    voice.insert(-1, abjad.Note(4.5, (1, 8)))

    assert abjad.wf.wellformed(voice)
    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            eqs'8
            f'8
            ]
        }
        """
    )


def test_Container_insert_06():
    """
    Insert works with really big negative values.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])
    voice.insert(-1000, abjad.Rest((1, 8)))

    assert abjad.wf.wellformed(voice)
    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            r8
            c'8
            [
            d'8
            e'8
            f'8
            ]
        }
        """
    )


def test_Container_insert_07():
    """
    Inserting a note from one container into another container
    changes note parent from first container to second.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")
    note = voice[0]
    staff.insert(1, voice[0])

    assert abjad.wf.wellformed(voice)
    assert abjad.wf.wellformed(staff)
    assert note not in voice
    assert note._parent is staff


def test_Container_insert_08():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.beam(staff[:])
    staff.insert(1, abjad.Note("cs'8"))

    assert abjad.wf.wellformed(staff)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            cs'8
            d'8
            e'8
            f'8
            ]
        }
        """
    )
