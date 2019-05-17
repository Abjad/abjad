import abjad
import pytest


def test_Mutation_split_01():
    """
    Cyclically splits note in score.
    """

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8"))
    staff.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'8
                [
                (
                d'8
                ]
            }
            {
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    notes = staff[0][1:2]
    result = abjad.mutate(notes).split([abjad.Duration(3, 64)], cyclic=True)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'8
                [
                (
                d'32.
                ~
                d'32.
                ~
                d'32
                ]
            }
            {
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()
    assert len(result) == 3


def test_Mutation_split_02():
    """
    Cyclically splits consecutive notes in score.
    """

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
                ]
            }
            {
                \time 2/8
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    result = abjad.mutate(leaves).split([abjad.Duration(3, 32)], cyclic=True)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'16.
                [
                (
                ~
                c'32
                d'16
                ~
                d'16
                ]
            }
            {
                \time 2/8
                e'32
                [
                ~
                e'16.
                f'16.
                ~
                f'32
                )
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()
    assert len(result) == 6


def test_Mutation_split_03():
    """
    Cyclically splits containers in score.
    """

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
                ]
            }
            {
                \time 2/8
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    measures = staff[:1]
    result = abjad.mutate(measures).split(
        [abjad.Duration(3, 32)], cyclic=True, tie_split_notes=False
    )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'16.
                [
                (
            }
            {
                c'32
                d'16
            }
            {
                d'16
                ]
            }
            {
                \time 2/8
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Mutation_split_04():
    """
    Cyclically splits consecutive measures in score.
    """

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
                ]
            }
            {
                \time 2/8
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    measures = staff[:]
    result = abjad.mutate(measures).split(
        [abjad.Duration(3, 32)], cyclic=True, tie_split_notes=False
    )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'16.
                [
                (
            }
            {
                c'32
                d'16
            }
            {
                d'16
                ]
            }
            {
                \time 2/8
                e'32
                [
            }
            {
                e'16.
            }
            {
                f'16.
            }
            {
                f'32
                )
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Mutation_split_05():
    """
    Cyclically splits orphan measures.
    """

    measures = [abjad.Container("c'8 d'8"), abjad.Container("e'8 f'8")]
    leaves = abjad.select(measures).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])

    result = abjad.mutate(measures).split(
        [abjad.Duration(3, 32)], cyclic=True, tie_split_notes=False
    )

    components = abjad.sequence(result).flatten(depth=-1)
    staff = abjad.Staff(components)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'16.
                [
            }
            {
                c'32
                d'16
            }
            {
                d'16
                ]
            }
            {
                e'32
                [
            }
            {
                e'16.
            }
            {
                f'16.
            }
            {
                f'32
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()
    assert len(result) == 6


def test_Mutation_split_06():
    """
    Cyclically splits note in score.
    """

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
                ]
            }
            {
                \time 2/8
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    notes = staff[0][1:]
    result = abjad.mutate(notes).split(
        [abjad.Duration(1, 32)], cyclic=True, tie_split_notes=True
    )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                [
                (
                d'32
                ~
                d'32
                ~
                d'32
                ~
                d'32
                ]
            }
            {
                \time 2/8
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()
    assert len(result) == 4


def test_Mutation_split_07():
    """
    Cyclically splits consecutive notes in score.
    """

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
                ]
            }
            {
                \time 2/8
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    result = abjad.mutate(leaves).split(
        [abjad.Duration(1, 16)], cyclic=True, tie_split_notes=True
    )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'16
                [
                (
                ~
                c'16
                d'16
                ~
                d'16
                ]
            }
            {
                \time 2/8
                e'16
                [
                ~
                e'16
                f'16
                ~
                f'16
                )
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()
    assert len(result) == 8


def test_Mutation_split_08():
    """
    Cyclically splits measure in score.
    """

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
                ]
            }
            {
                \time 2/8
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    measures = staff[:1]
    result = abjad.mutate(measures).split(
        [abjad.Duration(1, 16)], cyclic=True, tie_split_notes=True
    )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'16
                [
                (
                ~
            }
            {
                c'16
            }
            {
                d'16
                ~
            }
            {
                d'16
                ]
            }
            {
                \time 2/8
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()
    assert len(result) == 4


def test_Mutation_split_09():
    """
    Cyclically splits consecutive measures in score.
    """

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
                ]
            }
            {
                \time 2/8
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    measures = staff[:]
    result = abjad.mutate(measures).split(
        [abjad.Duration(3, 32)], cyclic=True, tie_split_notes=True
    )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'16.
                [
                (
                ~
            }
            {
                c'32
                d'16
                ~
            }
            {
                d'16
                ]
            }
            {
                \time 2/8
                e'32
                [
                ~
            }
            {
                e'16.
            }
            {
                f'16.
                ~
            }
            {
                f'32
                )
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()
    assert len(result) == 6


def test_Mutation_split_10():
    """
    Force-splits measure in score.
    """

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
                ]
            }
            {
                \time 2/8
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    measures = staff[:1]
    result = abjad.mutate(measures).split(
        [abjad.Duration(1, 32), abjad.Duration(3, 32), abjad.Duration(5, 32)],
        cyclic=False,
        tie_split_notes=False,
    )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'32
                [
                (
            }
            {
                c'16.
            }
            {
                d'8
                ]
            }
            {
                \time 2/8
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()
    assert len(result) == 3


def test_Mutation_split_11():
    """
    Force-splits consecutive measures in score.
    """

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
                ]
            }
            {
                \time 2/8
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    measures = staff[:]
    result = abjad.mutate(measures).split(
        [abjad.Duration(1, 32), abjad.Duration(3, 32), abjad.Duration(5, 32)],
        cyclic=False,
        tie_split_notes=False,
    )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'32
                [
                (
            }
            {
                c'16.
            }
            {
                d'8
                ]
            }
            {
                \time 2/8
                e'32
                [
            }
            {
                e'16.
                f'8
                )
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()
    assert len(result) == 4


def test_Mutation_split_12():
    """
    Splits tuplet in score
    """

    voice = abjad.Voice()
    voice.append(abjad.Tuplet((2, 3), "c'8 d'8 e'8"))
    voice.append(abjad.Tuplet((2, 3), "f'8 g'8 a'8"))
    leaves = abjad.select(voice).leaves()
    abjad.beam(leaves)

    tuplets = voice[1:2]
    result = abjad.mutate(tuplets).split([abjad.Duration(1, 12)])

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \times 2/3 {
                c'8
                [
                d'8
                e'8
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                f'8
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                g'8
                a'8
                ]
            }
        }
        """
    ), print(format(voice))

    assert abjad.inspect(voice).wellformed()


def test_Mutation_split_13():
    """
    Splits in-score measure with power-of-two denominator.
    """

    voice = abjad.Voice()
    voice.append(abjad.Container("c'8 d'8 e'8"))
    voice.append(abjad.Container("f'8 g'8 a'8"))
    leaves = abjad.select(voice).leaves()
    abjad.beam(leaves)

    measures = voice[1:2]
    result = abjad.mutate(measures).split([abjad.Duration(1, 8)])

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
                e'8
            }
            {
                f'8
            }
            {
                g'8
                a'8
                ]
            }
        }
        """
    ), print(format(voice))

    assert abjad.inspect(voice).wellformed()


def test_Mutation_split_14():
    """
    Splits container in middle.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")

    result = abjad.mutate([voice]).split([abjad.Duration(1, 4)])

    assert not len(voice)

    voice_1 = result[0][0]
    voice_2 = result[1][0]

    assert format(voice_1) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            d'8
        }
        """
    ), print(format(voice_1))

    assert abjad.inspect(voice_1).wellformed()

    assert format(voice_2) == abjad.String.normalize(
        r"""
        \new Voice
        {
            e'8
            f'8
        }
        """
    ), print(format(voice_2))

    assert abjad.inspect(voice_2).wellformed()


def test_Mutation_split_15():
    """
    Splits voice at negative index.
    """

    staff = abjad.Staff([abjad.Voice("c'8 d'8 e'8 f'8")])
    voice = staff[0]

    result = abjad.mutate([voice]).split([abjad.Duration(1, 4)])

    left = result[0][0]
    right = result[1][0]

    assert format(left) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            d'8
        }
        """
    ), print(format(left))

    assert format(right) == abjad.String.normalize(
        r"""
        \new Voice
        {
            e'8
            f'8
        }
        """
    ), print(format(right))

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
        }
        """
    ), print(format(voice))

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                c'8
                d'8
            }
            \new Voice
            {
                e'8
                f'8
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Mutation_split_16():
    """
    Splits container in score.
    """

    staff = abjad.Staff([abjad.Container("c'8 d'8 e'8 f'8")])
    voice = staff[0]
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves)

    result = abjad.mutate([voice]).split([abjad.Duration(1, 4)])

    left = result[0][0]
    right = result[1][0]

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

    assert format(left) == abjad.String.normalize(
        r"""
        {
            c'8
            [
            d'8
        }
        """
    ), print(format(left))

    assert format(right) == abjad.String.normalize(
        r"""
        {
            e'8
            f'8
            ]
        }
        """
    ), print(format(right))

    assert format(voice) == abjad.String.normalize(
        r"""
        {
        }
        """
    ), print(format(voice))

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

    assert abjad.inspect(staff).wellformed()


def test_Mutation_split_17():
    """
    Splits tuplet in score.
    """

    tuplet = abjad.Tuplet((4, 5), "c'8 c'8 c'8 c'8 c'8")
    voice = abjad.Voice([tuplet])
    staff = abjad.Staff([voice])
    abjad.beam(tuplet[:])

    result = abjad.mutate([tuplet]).split([abjad.Duration(1, 5)])

    left = result[0][0]
    right = result[1][0]

    assert format(left) == abjad.String.normalize(
        r"""
        \tweak edge-height #'(0.7 . 0)
        \times 4/5 {
            c'8
            [
            c'8
        }
        """
    ), print(format(left))

    assert format(right) == abjad.String.normalize(
        r"""
        \tweak edge-height #'(0.7 . 0)
        \times 4/5 {
            c'8
            c'8
            c'8
            ]
        }
        """
    ), print(format(right))

    assert format(tuplet) == abjad.String.normalize(
        r"""
        \times 4/5 {
        }
        """
    ), print(format(tuplet))

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \tweak edge-height #'(0.7 . 0)
            \times 4/5 {
                c'8
                [
                c'8
            }
            \tweak edge-height #'(0.7 . 0)
            \times 4/5 {
                c'8
                c'8
                c'8
                ]
            }
        }
        """
    ), print(format(voice))

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                \tweak edge-height #'(0.7 . 0)
                \times 4/5 {
                    c'8
                    [
                    c'8
                }
                \tweak edge-height #'(0.7 . 0)
                \times 4/5 {
                    c'8
                    c'8
                    c'8
                    ]
                }
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Mutation_split_18():
    """
    Splits cyclically.
    """

    voice = abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    leaves = abjad.select(voice).leaves()
    abjad.beam(leaves)
    abjad.slur(leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(format(voice))

    note = voice[0]
    result = abjad.mutate(note).split(
        [abjad.Duration(1, 8), abjad.Duration(3, 8)], cyclic=True
    )

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
            }
            {
                d'8
                e'8
                f'8
            }
            {
                g'8
            }
            {
                a'8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(format(voice))

    assert abjad.inspect(voice).wellformed()


def test_Mutation_split_19():
    """
    Cyclically splits all components in container.
    """

    voice = abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8")])
    leaves = abjad.select(voice).leaves()
    abjad.beam(leaves)
    abjad.slur(leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
                d'8
                e'8
                f'8
                )
                ]
            }
        }
        """
    ), print(format(voice))

    container = voice[0]
    result = abjad.mutate(container).split([abjad.Duration(1, 8)], cyclic=True)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
            }
            {
                d'8
            }
            {
                e'8
            }
            {
                f'8
                )
                ]
            }
        }
        """
    ), print(format(voice))

    assert abjad.inspect(voice).wellformed()


def test_Mutation_split_20():
    """
    Splits leaf at non-assignable, non-power-of-two offset.
    """

    staff = abjad.Staff("c'4")

    notes = staff[:1]
    result = abjad.mutate(notes).split([abjad.Duration(5, 24)])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                c'4
                ~
                c'16
                ~
                c'16
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()
