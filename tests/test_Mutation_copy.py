import abjad


def test_Mutation_copy_01():
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

    assert format(staff) == abjad.String.normalize(
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
    ), print(format(staff))

    result = abjad.mutate(leaves[2:4]).copy()
    new = abjad.Staff(result)

    assert format(new) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/8
            e'8
            f'8
        }
        """,
        print(format(new)),
    )
    assert abjad.wellformed(staff)
    assert abjad.wellformed(new)


def test_Mutation_copy_02():
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

    assert format(staff) == abjad.String.normalize(
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
    ), print(format(staff))

    result = abjad.mutate(staff[1:2]).copy()
    new = abjad.Staff(result)

    assert format(new) == abjad.String.normalize(
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
    ), print(format(new))

    assert abjad.wellformed(staff)
    assert abjad.wellformed(new)


def test_Mutation_copy_03():
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

    assert format(staff) == abjad.String.normalize(
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
    ), print(format(staff))

    result = abjad.mutate(leaves[-3:]).copy()
    new = abjad.Staff(result)

    assert format(new) == abjad.String.normalize(
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
    ), print(format(new))

    assert abjad.wellformed(staff)
    assert abjad.wellformed(new)


def test_Mutation_copy_04():

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
    ), print(format(staff))

    selection = abjad.select(staff)
    new_selection = abjad.mutate(selection).copy()
    new_staff = new_selection[0]

    assert format(new_staff) == abjad.String.normalize(
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
    ), print(format(new_staff))

    assert abjad.wellformed(new_staff)


def test_Mutation_copy_05():

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
    ), print(format(staff))

    result = abjad.mutate(staff[1:]).copy()
    new_staff = abjad.Staff(result)

    assert format(new_staff) == abjad.String.normalize(
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
    ), print(format(new_staff))

    assert abjad.wellformed(staff)
    assert abjad.wellformed(new_staff)


def test_Mutation_copy_06():

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
    ), print(format(staff))

    result = abjad.mutate(leaves[:6]).copy()
    new_staff = abjad.Staff(result)

    assert format(new_staff) == abjad.String.normalize(
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
    ), print(format(new_staff))

    assert abjad.wellformed(staff)
    assert abjad.wellformed(new_staff)


def test_Mutation_copy_07():

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
    ), print(format(staff))

    result = abjad.mutate(staff[-2:]).copy()
    new_staff = abjad.Staff(result)

    assert format(new_staff) == abjad.String.normalize(
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
    ), print(format(new_staff))

    assert abjad.wellformed(staff)
    assert abjad.wellformed(new_staff)


def test_Mutation_copy_08():
    """
    Copies hairpin.
    """

    staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    abjad.hairpin("< !", staff[:4])

    assert format(staff) == abjad.String.normalize(
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

    new_notes = abjad.mutate(staff[:4]).copy()
    staff.extend(new_notes)

    assert format(staff) == abjad.String.normalize(
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
    assert abjad.wellformed(staff)
