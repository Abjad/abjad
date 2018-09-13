import abjad


def test_Mutation_splice_01():

    voice = abjad.Voice("c'8 d'8 e'8")
    abjad.beam(voice[:])

    result = abjad.mutate(voice[-1]).splice(
        [abjad.Note("c'8"), abjad.Note("d'8"), abjad.Note("e'8")],
        grow_spanners=True,
        )

    assert abjad.inspect(voice).wellformed()
    assert result == voice[-4:]
    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            ]
            c'8
            d'8
            e'8
        }
        """
        ), print(format(voice))


def test_Mutation_splice_02():
    """
    Splices leaf after interior leaf.
    """

    voice = abjad.Voice("c'8 d'8 e'8")
    abjad.beam(voice[:])
    result = abjad.mutate(voice[1]).splice(
        [abjad.Note("dqs'8")],
        grow_spanners=True,
        )

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            dqs'8
            e'8
            ]
        }
        """
        ), print(format(voice))

    assert result == voice[1:3]
    assert abjad.inspect(voice).wellformed()


def test_Mutation_splice_03():
    """
    Splices tuplet after tuplet.
    """

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    voice = abjad.Voice([tuplet])
    abjad.beam(tuplet[:])
    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    result = abjad.mutate(voice[-1]).splice(
        [tuplet],
        grow_spanners=True,
        )

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
                c'8
                d'8
                e'8
            }
        }
        """
        ), print(format(voice))

    assert abjad.inspect(voice).wellformed()
    assert result == voice[:]


def test_Mutation_splice_04():
    """
    Splices after container with underspanners.
    """

    voice = abjad.Voice(abjad.Container("c'8 c'8") * 2)
    leaves = abjad.select(voice).leaves()
    abjad.beam(leaves)
    result = abjad.mutate(voice[0]).splice(
        [abjad.Note("dqs'8")],
        grow_spanners=True,
        )

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                c'8
            }
            dqs'8
            {
                c'8
                c'8
                ]
            }
        }
        """
        ), print(format(voice))

    assert abjad.inspect(voice).wellformed()
    assert result == voice[0:2]


def test_Mutation_splice_05():
    """
    Extends leaves rightwards after leaf.
    """

    voice = abjad.Voice("c'8 d'8 e'8")
    abjad.beam(voice[:])

    result = abjad.mutate(voice[-1]).splice(
        [abjad.Note("c'8"), abjad.Note("d'8"), abjad.Note("e'8")],
        grow_spanners=False,
        )

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            ]
            c'8
            d'8
            e'8
        }
        """
        ), print(format(voice))

    assert abjad.inspect(voice).wellformed()
    assert result == voice[-4:]


def test_Mutation_splice_06():
    """
    Extends leaf rightwards after interior leaf.
    """

    voice = abjad.Voice("c'8 d'8 e'8")
    abjad.beam(voice[:])

    result = abjad.mutate(voice[1]).splice(
        [abjad.Note("dqs'8")],
        grow_spanners=False,
        )

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            dqs'8
            e'8
            ]
        }
        """
        ), print(format(voice))

    assert result == voice[1:3]
    assert abjad.inspect(voice).wellformed()


def test_Mutation_splice_07():
    """
    Splices leaves left of leaf.
    """

    voice = abjad.Voice("c'8 d'8 e'8")
    abjad.beam(voice[:])
    notes = [abjad.Note("c'16"), abjad.Note("d'16"), abjad.Note("e'16")]
    result = abjad.mutate(voice[0]).splice(
        notes,
        direction=abjad.Left,
        grow_spanners=True,
        )

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'16
            d'16
            e'16
            c'8
            [
            d'8
            e'8
            ]
        }
        """
        ), print(format(voice))

    assert abjad.inspect(voice).wellformed()
    assert result == voice[:4]


def test_Mutation_splice_08():
    """
    Splices leaf left of interior leaf.
    """

    voice = abjad.Voice("c'8 d'8 e'8")
    abjad.beam(voice[:])
    result = abjad.mutate(voice[1]).splice(
        [abjad.Note("dqf'8")],
        direction=abjad.Left,
        grow_spanners=True,
        )

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            dqf'8
            d'8
            e'8
            ]
        }
        """
        ), print(format(voice))

    assert abjad.inspect(voice).wellformed()
    assert result == voice[1:3]


def test_Mutation_splice_09():
    """
    Splices tuplet left of tuplet.
    """

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    voice = abjad.Voice([tuplet])
    abjad.beam(tuplet[:])
    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    result = abjad.mutate(voice[0]).splice(
        [tuplet],
        direction=abjad.Left,
        grow_spanners=True,
        )

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            \times 2/3 {
                c'8
                [
                d'8
                e'8
                ]
            }
        }
        """
        ), print(format(voice))

    assert abjad.inspect(voice).wellformed()
    assert result == voice[:]


def test_Mutation_splice_10():
    """
    Splices left of container with underspanners.
    """

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select(voice).leaves()
    abjad.beam(leaves)
    result = abjad.mutate(voice[1]).splice(
        [abjad.Note("dqs'8")],
        direction=abjad.Left,
        grow_spanners=True,
        )

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
            dqs'8
            {
                e'8
                f'8
                ]
            }
        }
        """
        ), print(format(voice))

    assert result == voice[1:]
    assert abjad.inspect(voice).wellformed()


def test_Mutation_splice_11():
    """
    Extends leaves leftwards of leaf. Do not extend edge spanners.
    """

    voice = abjad.Voice("c'8 d'8 e'8")
    abjad.beam(voice[:])
    notes = [abjad.Note("c'16"), abjad.Note("d'16"), abjad.Note("e'16")]
    result = abjad.mutate(voice[0]).splice(
        notes,
        direction=abjad.Left,
        grow_spanners=False,
        )

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'16
            d'16
            e'16
            c'8
            [
            d'8
            e'8
            ]
        }
        """
        ), print(format(voice))

    assert abjad.inspect(voice).wellformed()
    assert result == voice[:4]


def test_Mutation_splice_12():
    """
    Extends leaf leftwards of interior leaf. Does extend interior spanners.
    """

    voice = abjad.Voice("c'8 d'8 e'8")
    abjad.beam(voice[:])
    result = abjad.mutate(voice[1]).splice(
        [abjad.Note("dqf'8")],
        direction=abjad.Left,
        grow_spanners=False,
        )

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            dqf'8
            d'8
            e'8
            ]
        }
        """
        ), print(format(voice))

    assert result == voice[1:3]
    assert abjad.inspect(voice).wellformed()
