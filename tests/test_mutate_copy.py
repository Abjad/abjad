import abjad


def test_mutate_copy_01():
    """
    Deep copies components.
    Returns Python list of copied components.
    """

    staff = abjad.Staff(
        [
            abjad.Container("c'8 d'"),
            abjad.Container("e'8 f'"),
            abjad.Container("g'8 a'"),
        ]
    )
    for container in staff:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select(staff).leaves()
    abjad.slur(leaves)
    abjad.trill_spanner(leaves)
    abjad.beam(leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                (
                \startTrillSpan
                [
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
                )
                \stopTrillSpan
                ]
            }
        }
        """
    ), print(abjad.lilypond(staff))

    result = abjad.mutate.copy(leaves[2:4])
    new = abjad.Staff(result)

    assert abjad.lilypond(new) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/8
            e'8
            f'8
        }
        """,
        print(abjad.lilypond(new)),
    )
    assert abjad.wf.wellformed(staff)
    assert abjad.wf.wellformed(new)


def test_mutate_copy_02():
    """
    Copy one measure.
    """

    staff = abjad.Staff(
        [
            abjad.Container("c'8 d'"),
            abjad.Container("e'8 f'"),
            abjad.Container("g'8 a'"),
        ]
    )
    for container in staff:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select(staff).leaves()
    abjad.slur(leaves)
    abjad.trill_spanner(leaves)
    abjad.beam(leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                (
                \startTrillSpan
                [
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
                )
                \stopTrillSpan
                ]
            }
        }
        """
    ), print(abjad.lilypond(staff))

    result = abjad.mutate.copy(staff[1:2])
    new = abjad.Staff(result)

    assert abjad.lilypond(new) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                e'8
                f'8
            }
        }
        """
    ), print(abjad.lilypond(new))

    assert abjad.wf.wellformed(staff)
    assert abjad.wf.wellformed(new)


def test_mutate_copy_03():
    """
    Three notes crossing measure boundaries.
    """

    staff = abjad.Staff(
        [
            abjad.Container("c'8 d'"),
            abjad.Container("e'8 f'"),
            abjad.Container("g'8 a'"),
        ]
    )
    for container in staff:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select(staff).leaves()
    abjad.slur(leaves)
    abjad.trill_spanner(leaves)
    abjad.beam(leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                (
                \startTrillSpan
                [
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
                )
                \stopTrillSpan
                ]
            }
        }
        """
    ), print(abjad.lilypond(staff))

    result = abjad.mutate.copy(leaves[-3:])
    new = abjad.Staff(result)

    assert abjad.lilypond(new) == abjad.String.normalize(
        r"""
        \new Staff
        {
            f'8
            \time 2/8
            g'8
            a'8
            )
            \stopTrillSpan
            ]
        }
        """
    ), print(abjad.lilypond(new))

    assert abjad.wf.wellformed(staff)
    assert abjad.wf.wellformed(new)


def test_mutate_copy_04():

    staff = abjad.Staff(
        [
            abjad.Container("c'8 d'"),
            abjad.Container("e'8 f'"),
            abjad.Container("g'8 a'"),
            abjad.Container("b'8 c''"),
        ]
    )
    for container in staff:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves)
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
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(staff))

    selection = abjad.select(staff)
    new_selection = abjad.mutate.copy(selection)
    new_staff = new_selection[0]

    assert abjad.lilypond(new_staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                [
                (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(new_staff))

    assert abjad.wf.wellformed(new_staff)


def test_mutate_copy_05():

    staff = abjad.Staff(
        [
            abjad.Container("c'8 d'"),
            abjad.Container("e'8 f'"),
            abjad.Container("g'8 a'"),
            abjad.Container("b'8 c''"),
        ]
    )
    for container in staff:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves)
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
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(staff))

    result = abjad.mutate.copy(staff[1:])
    new_staff = abjad.Staff(result)

    assert abjad.lilypond(new_staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(new_staff))

    assert abjad.wf.wellformed(staff)
    assert abjad.wf.wellformed(new_staff)


def test_mutate_copy_06():

    staff = abjad.Staff(
        [
            abjad.Container("c'8 d'"),
            abjad.Container("e'8 f'"),
            abjad.Container("g'8 a'"),
            abjad.Container("b'8 c''"),
        ]
    )
    for container in staff:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves)
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
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(staff))

    result = abjad.mutate.copy(leaves[:6])
    new_staff = abjad.Staff(result)

    assert abjad.lilypond(new_staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/8
            c'8
            [
            (
            d'8
            \time 2/8
            e'8
            f'8
            \time 2/8
            g'8
            a'8
        }
        """
    ), print(abjad.lilypond(new_staff))

    assert abjad.wf.wellformed(staff)
    assert abjad.wf.wellformed(new_staff)


def test_mutate_copy_07():

    staff = abjad.Staff(
        [
            abjad.Container("c'8 d'"),
            abjad.Container("e'8 f'"),
            abjad.Container("g'8 a'"),
            abjad.Container("b'8 c''"),
        ]
    )
    for container in staff:
        time_signature = abjad.TimeSignature((2, 8))
        abjad.attach(time_signature, container[0])
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves)
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
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(staff))

    result = abjad.mutate.copy(staff[-2:])
    new_staff = abjad.Staff(result)

    assert abjad.lilypond(new_staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(new_staff))

    assert abjad.wf.wellformed(staff)
    assert abjad.wf.wellformed(new_staff)


def test_mutate_copy_08():
    """
    Copies hairpin.
    """

    staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    abjad.hairpin("< !", staff[:4])

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            \<
            cs'8
            d'8
            ef'8
            \!
            e'8
            f'8
            fs'8
            g'8
        }
        """
    )

    new_notes = abjad.mutate.copy(staff[:4])
    staff.extend(new_notes)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            \<
            cs'8
            d'8
            ef'8
            \!
            e'8
            f'8
            fs'8
            g'8
            c'8
            \<
            cs'8
            d'8
            ef'8
            \!
        }
        """
    )
    assert abjad.wf.wellformed(staff)
