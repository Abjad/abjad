import pytest

import abjad


def test_Container_append_01():
    """
    Append sequential to voice.
    """

    voice = abjad.Voice("c'8 d'8")
    abjad.beam(voice[:])
    voice.append(abjad.Container("e'8 f'8"))

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            {
                e'8
                f'8
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_Container_append_02():
    """
    Append leaf to tuplet.
    """

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    abjad.beam(tuplet[:])
    tuplet.append(abjad.Note(5, (1, 16)), preserve_duration=True)

    assert abjad.lilypond(tuplet) == abjad.String.normalize(
        r"""
        \times 4/7 {
            c'8
            [
            d'8
            e'8
            ]
            f'16
        }
        """
    ), print(abjad.lilypond(tuplet))

    assert abjad.wf.wellformed(tuplet)


def test_Container_append_03():
    """
    Trying to append noncomponent to container raises TypeError.
    """

    voice = abjad.Voice("c'8 d'8 e'8")
    abjad.beam(voice[:])

    with pytest.raises(Exception):
        voice.append("foo")
    with pytest.raises(Exception):
        voice.append(99)
    with pytest.raises(Exception):
        voice.append([])
    with pytest.raises(Exception):
        voice.append([abjad.Note(0, (1, 8))])


def test_Container_append_04():
    """
    Append spanned leaf from donor container to recipient container.
    """

    voice_1 = abjad.Voice("c'8 d'8 e'8")
    abjad.beam(voice_1[:])

    assert abjad.lilypond(voice_1) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            ]
        }
        """
    ), print(abjad.lilypond(voice_1))

    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice_2[:])

    assert abjad.lilypond(voice_2) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(voice_2))

    voice_1.append(voice_2[-1])

    assert abjad.lilypond(voice_1) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            ]
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(voice_1))

    assert abjad.wf.wellformed(voice_1)

    assert abjad.lilypond(voice_2) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
        }
        """
    ), print(abjad.lilypond(voice_2))

    assert abjad.wf.wellformed(voice_2)


def test_Container_append_05():
    """
    Append spanned leaf from donor container to recipient container.
    Donor and recipient containers are the same.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:])

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(voice))

    voice.append(voice[1])

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            e'8
            f'8
            ]
            d'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_Container_append_06():
    """
    Can not insert grace container into container.
    """

    staff = abjad.Staff("c' d' e'")
    grace_container = abjad.BeforeGraceContainer("f'16 g'")

    with pytest.raises(Exception):
        staff.append(grace_container)
