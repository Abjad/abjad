import pytest

import abjad


def test_Mutation_swap_01():
    """
    Moves parentage, children from multiple containers to empty tuplet.
    """

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
                ]
            }
        }
        """
    )

    tuplet = abjad.Tuplet("4:3", [])
    abjad.mutate.swap(voice[:2], tuplet)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \tuplet 4/3
            {
                c'8
                [
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8
                ]
            }
        }
        """
    )

    assert abjad.wf.is_wellformed(voice, do_not_check_overlapping_beams=True)


def test_Mutation_swap_02():
    """
    Moves parentage, children from container to empty voice.
    """

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select.leaves(voice)
    voice.set_name("foo")
    abjad.beam(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \context Voice = "foo"
        {
            {
                c'8
                [
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
                ]
            }
        }
        """
    )

    new_voice = abjad.Voice()
    new_voice.set_name("foo")
    abjad.mutate.swap(voice[1:2], new_voice)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \context Voice = "foo"
        {
            {
                c'8
                [
                d'8
            }
            \context Voice = "foo"
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
                ]
            }
        }
        """
    )

    assert abjad.wf.is_wellformed(voice)


def test_Mutation_swap_03():
    """
    Moves parentage, children from container to empty tuplet.
    """

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
                ]
            }
        }
        """
    )

    tuplet = abjad.Tuplet("4:3", [])
    abjad.mutate.swap(voice[1:2], tuplet)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
            \tuplet 4/3
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
                ]
            }
        }
        """
    )

    assert abjad.wf.is_wellformed(voice)


def test_Mutation_swap_04():
    """
    Raises exception when Trying to move parentage, children to noncontainer.
    """

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)

    note = abjad.Note("c'4")
    with pytest.raises(Exception):
        abjad.mutate.swap(voice[1:2], note)


def test_Mutation_swap_05():
    """
    Raises exception when trying to move parentage, children from nonempty
    container to nonempty container.
    """

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)

    tuplet = abjad.Tuplet("3:2", "c'8 d'8 e'8")
    with pytest.raises(Exception):
        abjad.mutate.swap(voice[1:2], tuplet)


def test_Mutation_swap_06():
    """
    Raises exception when Trying to move parentage, children from components
    that are not parent-contiguous.
    """

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
                ]
            }
        }
        """
    )

    tuplet = abjad.Tuplet("3:2", [])
    with pytest.raises(Exception):
        abjad.mutate.swap([voice[0], voice[2]], tuplet)


def test_Mutation_swap_07():
    """
    Moves parentage, children from one container to another.
    """

    measure = abjad.Container("c'8 d'8 e'8 f'8")

    assert abjad.lilypond(measure) == abjad.string.normalize(
        r"""
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    new_measure = abjad.Container()
    abjad.mutate.swap(measure, new_measure)

    assert abjad.lilypond(new_measure) == abjad.string.normalize(
        r"""
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    assert abjad.wf.is_wellformed(new_measure)
