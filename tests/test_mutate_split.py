import abjad


def test_mutate_split_01():
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

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    notes = staff[0][1:2]
    result = abjad.mutate.split(notes, [abjad.Duration(3, 64)], cyclic=True)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 3


def test_mutate_split_02():
    """
    Cyclically splits consecutive notes in score.
    """

    staff = abjad.Staff([abjad.Container("c'8 d'"), abjad.Container("e'8 f'")])
    for container in staff:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    result = abjad.mutate.split(leaves, [abjad.Duration(3, 32)], cyclic=True)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 6


def test_mutate_split_03():
    """
    Cyclically splits note in score.
    """

    staff = abjad.Staff([abjad.Container("c'8 d'"), abjad.Container("e'8 f'")])
    for container in staff:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    notes = staff[0][1:]
    result = abjad.mutate.split(notes, [abjad.Duration(1, 32)], cyclic=True)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 4


def test_mutate_split_04():
    """
    Cyclically splits consecutive notes in score.
    """

    staff = abjad.Staff([abjad.Container("c'8 d'"), abjad.Container("e'8 f'")])
    for container in staff:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    result = abjad.mutate.split(leaves, [abjad.Duration(1, 16)], cyclic=True)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 8


def test_mutate_split_05():
    """
    Cyclically splits measure in score.
    """

    staff = abjad.Staff([abjad.Container("c'8 d'"), abjad.Container("e'8 f'")])
    for container in staff:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    measures = staff[:1]
    result = abjad.mutate.split(measures, [abjad.Duration(1, 16)], cyclic=True)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 4


def test_mutate_split_06():
    """
    Cyclically splits consecutive measures in score.
    """

    staff = abjad.Staff([abjad.Container("c'8 d'"), abjad.Container("e'8 f'")])
    for container in staff:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    measures = staff[:]
    result = abjad.mutate.split(measures, [abjad.Duration(3, 32)], cyclic=True)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 6


def test_mutate_split_07():
    """
    Splits tuplet in score
    """

    voice = abjad.Voice()
    voice.append(abjad.Tuplet((2, 3), "c'8 d'8 e'8"))
    voice.append(abjad.Tuplet((2, 3), "f'8 g'8 a'8"))
    leaves = abjad.select(voice).leaves()
    abjad.beam(leaves)

    tuplets = voice[1:2]
    abjad.mutate.split(tuplets, [abjad.Duration(1, 12)])

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_split_08():
    """
    Splits in-score measure with power-of-two denominator.
    """

    voice = abjad.Voice()
    voice.append(abjad.Container("c'8 d'8 e'8"))
    voice.append(abjad.Container("f'8 g'8 a'8"))
    leaves = abjad.select(voice).leaves()
    abjad.beam(leaves)

    measures = voice[1:2]
    abjad.mutate.split(measures, [abjad.Duration(1, 8)])

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_split_09():
    """
    Splits container in middle.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")

    result = abjad.mutate.split([voice], [abjad.Duration(1, 4)])

    assert not len(voice)

    voice_1 = result[0][0]
    voice_2 = result[1][0]

    assert abjad.lilypond(voice_1) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            d'8
        }
        """
    ), print(abjad.lilypond(voice_1))

    assert abjad.wf.wellformed(voice_1)

    assert abjad.lilypond(voice_2) == abjad.String.normalize(
        r"""
        \new Voice
        {
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice_2))

    assert abjad.wf.wellformed(voice_2)


def test_mutate_split_10():
    """
    Splits voice at negative index.
    """

    staff = abjad.Staff([abjad.Voice("c'8 d'8 e'8 f'8")])
    voice = staff[0]

    result = abjad.mutate.split([voice], [abjad.Duration(1, 4)])

    left = result[0][0]
    right = result[1][0]

    assert abjad.lilypond(left) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            d'8
        }
        """
    ), print(abjad.lilypond(left))

    assert abjad.lilypond(right) == abjad.String.normalize(
        r"""
        \new Voice
        {
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(right))

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_mutate_split_11():
    """
    Splits container in score.
    """

    staff = abjad.Staff([abjad.Container("c'8 d'8 e'8 f'8")])
    voice = staff[0]
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves)

    result = abjad.mutate.split([voice], [abjad.Duration(1, 4)])

    left = result[0][0]
    right = result[1][0]

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

    assert abjad.lilypond(left) == abjad.String.normalize(
        r"""
        {
            c'8
            [
            d'8
        }
        """
    ), print(abjad.lilypond(left))

    assert abjad.lilypond(right) == abjad.String.normalize(
        r"""
        {
            e'8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(right))

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        {
        }
        """
    ), print(abjad.lilypond(voice))

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

    assert abjad.wf.wellformed(staff)


def test_mutate_split_12():
    """
    Splits tuplet in score.
    """

    tuplet = abjad.Tuplet((4, 5), "c'8 c'8 c'8 c'8 c'8")
    voice = abjad.Voice([tuplet])
    staff = abjad.Staff([voice])
    abjad.beam(tuplet[:])

    result = abjad.mutate.split([tuplet], [abjad.Duration(1, 5)])

    left = result[0][0]
    right = result[1][0]

    assert abjad.lilypond(left) == abjad.String.normalize(
        r"""
        \tweak edge-height #'(0.7 . 0)
        \times 4/5 {
            c'8
            [
            c'8
        }
        """
    ), print(abjad.lilypond(left))

    assert abjad.lilypond(right) == abjad.String.normalize(
        r"""
        \tweak edge-height #'(0.7 . 0)
        \times 4/5 {
            c'8
            c'8
            c'8
            ]
        }
        """
    ), print(abjad.lilypond(right))

    assert abjad.lilypond(tuplet) == abjad.String.normalize(
        r"""
        \times 4/5 {
        }
        """
    ), print(abjad.lilypond(tuplet))

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    ), print(abjad.lilypond(voice))

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_mutate_split_13():
    """
    Splits cyclically.
    """

    voice = abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    leaves = abjad.select(voice).leaves()
    abjad.beam(leaves)
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    ), print(abjad.lilypond(voice))

    note = voice[0]
    abjad.mutate.split(note, [abjad.Duration(1, 8), abjad.Duration(3, 8)], cyclic=True)

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_split_14():
    """
    Cyclically splits all components in container.
    """

    voice = abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8")])
    leaves = abjad.select(voice).leaves()
    abjad.beam(leaves)
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    ), print(abjad.lilypond(voice))

    container = voice[0]
    abjad.mutate.split(container, [abjad.Duration(1, 8)], cyclic=True)

    assert abjad.lilypond(voice) == abjad.String.normalize(
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
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_split_15():
    """
    Splits leaf at non-assignable, non-power-of-two offset.
    """

    staff = abjad.Staff("c'4")

    notes = staff[:1]
    abjad.mutate.split(notes, [abjad.Duration(5, 24)])

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
