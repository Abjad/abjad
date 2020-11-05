import pytest

import abjad


def test_Container_extend_01():
    """
    Extend container with list of leaves.
    """

    voice = abjad.Voice("c'8 d'8")
    abjad.beam(voice[:])
    voice.extend([abjad.Note("c'8"), abjad.Note("d'8")])

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            c'8
            d'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_Container_extend_02():
    """
    Extend container with contents of other container.
    """

    voice_1 = abjad.Voice("c'8 d'8")
    abjad.beam(voice_1[:])

    voice_2 = abjad.Voice("e'8 f'8")
    abjad.beam(voice_2[:])
    voice_1.extend(voice_2)

    assert abjad.lilypond(voice_1) == abjad.String.normalize(
        r"""
        \new Voice
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
    ), print(abjad.lilypond(voice_1))

    assert abjad.wf.wellformed(voice_1)


def test_Container_extend_03():
    """
    Extending container with empty list leaves container unchanged.
    """

    voice = abjad.Voice("c'8 d'8")
    abjad.beam(voice[:])
    voice.extend([])

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_Container_extend_04():
    """
    Extending one container with empty second container leaves both
    containers unchanged.
    """

    voice = abjad.Voice("c'8 d'8")
    abjad.beam(voice[:])
    voice.extend(abjad.Voice([]))

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_Container_extend_05():
    """
    Trying to extend container with noncomponent raises TypeError.
    """

    voice = abjad.Voice("c'8 d'8")
    abjad.beam(voice[:])

    with pytest.raises(Exception):
        voice.extend(7)
    with pytest.raises(Exception):
        voice.extend("foo")


def test_Container_extend_06():
    """
    Trying to extend container with noncontainer raises exception.
    """

    voice = abjad.Voice("c'8 d'8")
    abjad.beam(voice[:])

    with pytest.raises(AttributeError):
        voice.extend(abjad.Note(4, (1, 4)))

    with pytest.raises(AttributeError):
        voice.extend(abjad.Chord([2, 3, 5], (1, 4)))


def test_Container_extend_07():
    """
    Extend container with partial and spanned contents of other container.
    """

    voice_1 = abjad.Voice("c'8 d'8")
    abjad.beam(voice_1[:])

    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice_2[:])

    voice_1.extend(voice_2[-2:])

    assert abjad.lilypond(voice_1) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            e'8
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
        }
        """
    ), print(abjad.lilypond(voice_2))

    assert abjad.wf.wellformed(voice_2)


def test_Container_extend_08():
    """
    Extend container with partial and spanned contents of other container.
    Covered span comes with components from donor container.
    """

    voice_1 = abjad.Voice("c'8 d'8")
    abjad.beam(voice_1[:])

    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice_2[:])
    abjad.slur(voice_2[-2:])

    assert abjad.lilypond(voice_2) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            (
            f'8
            )
            ]
        }
        """
    ), print(abjad.lilypond(voice_2))

    voice_1.extend(voice_2[-2:])

    assert abjad.lilypond(voice_1) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            e'8
            (
            f'8
            )
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
        }
        """
    ), print(abjad.lilypond(voice_2))

    assert abjad.wf.wellformed(voice_2)


def test_Container_extend_09():
    """
    Extend container with LilyPond input string.
    """

    container = abjad.Container([])
    container.extend("c'4 ( d'4 e'4 f'4 )")

    assert abjad.lilypond(container) == abjad.String.normalize(
        r"""
        {
            c'4
            (
            d'4
            e'4
            f'4
            )
        }
        """
    ), print(abjad.lilypond(container))

    assert abjad.wf.wellformed(container)


def test_Container_extend_10():
    """
    Selections are stripped out.
    """

    maker = abjad.NoteMaker()
    selection_1 = maker([0, 2], [abjad.Duration(1, 4)])
    selection_2 = maker([4, 5], [abjad.Duration(1, 4)])
    selection_3 = maker([7, 9], [abjad.Duration(1, 4)])
    selection_4 = maker([11, 12], [abjad.Duration(1, 4)])
    selections = [selection_1, selection_2, selection_3, selection_4]
    container = abjad.Container()
    container.extend(selections)

    assert abjad.lilypond(container) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
            g'4
            a'4
            b'4
            c''4
        }
        """
    ), print(abjad.lilypond(container))

    assert abjad.wf.wellformed(container)
