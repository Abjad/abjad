import abjad
import pytest


def test_Mutation_fuse_01():
    """
    Works with list of leaves.
    """

    notes = 8 * abjad.Note("c'4")
    fused = abjad.mutate(notes).fuse()

    assert len(fused) == 1
    assert fused[0].written_duration == abjad.Duration(2)


def test_Mutation_fuse_02():
    """
    Works with Leaf component.
    """

    fused = abjad.mutate(abjad.Note("c'4")).fuse()
    assert len(fused) == 1
    assert fused[0].written_duration == abjad.Duration(1, 4)


def test_Mutation_fuse_03():
    """
    Works with containers.
    """

    voice = abjad.Voice(8 * abjad.Note("c'4"))
    fused = abjad.mutate(voice[:]).fuse()
    assert len(fused) == 1
    assert fused[0].written_duration == 2
    assert voice[0] is fused[0]


def test_Mutation_fuse_04():
    """
    Fusion results in tied notes.
    """

    voice = abjad.Voice([abjad.Note(0, (2, 16)), abjad.Note(9, (3, 16))])
    fused = abjad.mutate(voice[:]).fuse()

    assert len(fused) == 2
    assert fused[0].written_duration == abjad.Duration(1, 4)
    assert fused[1].written_duration == abjad.Duration(1, 16)

    tie_1 = abjad.inspect(fused[0]).spanner(abjad.Tie)
    tie_2 = abjad.inspect(fused[1]).spanner(abjad.Tie)

    assert tie_1 is tie_2
    assert voice[0] is fused[0]
    assert voice[1] is fused[1]
    assert voice[0].written_pitch == voice[1].written_pitch


def test_Mutation_fuse_05():
    """
    Fuses leaves with differing LilyPond multipliers.
    """

    staff = abjad.Staff([abjad.Skip((1, 1)), abjad.Skip((1, 1))])
    staff[0].multiplier = (1, 16)
    staff[1].multiplier = (5, 16)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            s1 * 1/16
            s1 * 5/16
        }
        """
        )

    assert abjad.inspect(staff).duration() == abjad.Duration(3, 8)

    abjad.mutate(staff[:]).fuse()

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            s1 * 3/8
        }
        """
        )

    assert abjad.inspect(staff).duration() == abjad.Duration(3, 8)
    assert abjad.inspect(staff).wellformed()


def test_Mutation_fuse_06():
    """
    Fuses two unincorporated tuplets with same multiplier.
    """

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    beam = abjad.Beam()
    abjad.attach(beam, tuplet_1[:])
    tuplet_2 = abjad.Tuplet((2, 3), "c'16 d'16 e'16")
    slur = abjad.Slur()
    abjad.attach(slur, tuplet_2[:])

    assert format(tuplet_1) == abjad.String.normalize(
        r"""
        \times 2/3 {
            c'8
            [
            d'8
            e'8
            ]
        }
        """
        )

    assert format(tuplet_2) == abjad.String.normalize(
        r"""
        \times 2/3 {
            c'16
            (
            d'16
            e'16
            )
        }
        """
        )

    tuplets = abjad.select([tuplet_1, tuplet_2])
    new = abjad.mutate(tuplets).fuse()

    assert format(new) == abjad.String.normalize(
        r"""
        \times 2/3 {
            c'8
            [
            d'8
            e'8
            ]
            c'16
            (
            d'16
            e'16
            )
        }
        """
        )

    assert len(tuplet_1) == 0
    assert len(tuplet_2) == 0
    assert new is not tuplet_1 and new is not tuplet_2
    assert abjad.inspect(new).wellformed()


def test_Mutation_fuse_07():
    """
    Fuses tuplets with same multiplier in score.
    """

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    beam = abjad.Beam()
    abjad.attach(beam, tuplet_1[:])
    tuplet_2 = abjad.Tuplet((2, 3), "c'16 d'16 e'16")
    slur = abjad.Slur()
    abjad.attach(slur, tuplet_2[:])
    voice = abjad.Voice([tuplet_1, tuplet_2])

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \times 2/3 {
                c'8
                [
                d'8
                e'8
                ]
            }
            \times 2/3 {
                c'16
                (
                d'16
                e'16
                )
            }
        }
        """
        )

    tuplets = voice[:]
    abjad.mutate(tuplets).fuse()

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \times 2/3 {
                c'8
                [
                d'8
                e'8
                ]
                c'16
                (
                d'16
                e'16
                )
            }
        }
        """
        )

    assert abjad.inspect(voice).wellformed()


def test_Mutation_fuse_08():
    """
    Fuses fixed-multiplier tuplets with same multiplier in score.
    """

    tuplet_1 = abjad.Tuplet(abjad.Multiplier(2, 3), "c'8 d'8 e'8")
    beam = abjad.Beam()
    abjad.attach(beam, tuplet_1[:])
    tuplet_2 = abjad.Tuplet(abjad.Multiplier(2, 3), "c'8 d'8 e'8 f'8 g'8")
    slur = abjad.Slur()
    abjad.attach(slur, tuplet_2[:])
    voice = abjad.Voice([tuplet_1, tuplet_2])

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \times 2/3 {
                c'8
                [
                d'8
                e'8
                ]
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8
                (
                d'8
                e'8
                f'8
                g'8
                )
            }
        }
        """
        )

    tuplets = voice[:]
    abjad.mutate(tuplets).fuse()

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8
                [
                d'8
                e'8
                ]
                c'8
                (
                d'8
                e'8
                f'8
                g'8
                )
            }
        }
        """
        )

    assert abjad.inspect(voice).wellformed()


def test_Mutation_fuse_09():
    """
    Tuplets must carry same multiplier.
    """

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    tuplet_2 = abjad.Tuplet ((4, 5), "c'8 d'8 e'8 f'8 g'8")
    tuplets = abjad.select([tuplet_1, tuplet_2])

    assert pytest.raises(Exception, 'abjad.mutate(tuplets).fuse()')


def test_Mutation_fuse_10():
    """
    Dominant spanners on contents are preserved.
    """

    tuplet_1 = abjad.Tuplet((2, 3), "c'8")
    tuplet_2 = abjad.Tuplet((2, 3), "c'4")
    voice = abjad.Voice([tuplet_1, tuplet_2, abjad.Note("c'4")])
    leaves = abjad.select(voice).leaves()
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8
                (
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'4
            }
            c'4
            )
        }
        """
        )

    tuplets = voice[:2]
    abjad.mutate(tuplets).fuse()

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \times 2/3 {
                c'8
                (
                c'4
            }
            c'4
            )
        }
        """
        )

    assert abjad.inspect(voice).wellformed()


def test_Mutation_fuse_11():
    """
    Fusing empty selection returns none.
    """

    staff = abjad.Staff()
    result = abjad.mutate(staff[:]).fuse()
    assert result == abjad.Selection()
