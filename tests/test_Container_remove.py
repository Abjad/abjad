import pytest

import abjad


def test_Container_remove_01():
    """
    Containers remove leaves correctly.
    Leaf abjad.detaches from parentage.
    Leaf returns after removal.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.slur(voice[:])
    abjad.beam(voice[1:2], beam_lone_notes=True)

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            (
            d'8
            [
            ]
            e'8
            f'8
            )
        }
        """
    )

    note = voice[1]
    voice.remove(note)

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            (
            e'8
            f'8
            )
        }
        """
    )

    "Note is now d'8 [ ]"

    assert abjad.lilypond(note) == "d'8\n[\n]"

    assert abjad.wf.wellformed(voice)
    assert abjad.wf.wellformed(note)


def test_Container_remove_02():
    """
    Containers remove nested containers correctly.
    abjad.Container abjad.detaches from parentage.
    abjad.Container returns after removal.
    """

    staff = abjad.Staff("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select(staff).leaves()
    sequential = staff[0]
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
    )

    staff.remove(sequential)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                e'8
                f'8
                ]
            }
        }
        """
    )

    assert abjad.wf.wellformed(staff)

    assert abjad.lilypond(sequential) == abjad.String.normalize(
        r"""
        {
            c'8
            [
            d'8
        }
        """
    )

    assert abjad.wf.wellformed(sequential)


def test_Container_remove_03():
    """
    Container remove works on identity and not equality.
    """

    note = abjad.Note("c'4")
    container = abjad.Container([abjad.Note("c'4")])

    with pytest.raises(Exception):
        container.remove(note)
