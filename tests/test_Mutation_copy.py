import abjad


def test_Mutation_copy_01():
    """
    Deep copies components.
    Deep copies spanners that abjad.attach to client.
    Fractures spanners that abjad.attach to components not in client.
    Returns Python list of copied components.
    """

    staff = abjad.Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
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
        """, print(format(new))
        )
    assert abjad.inspect(staff).wellformed()
    assert abjad.inspect(new).wellformed()


def test_Mutation_copy_02():
    """
    Copy one measure and fracture spanners.
    """

    staff = abjad.Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
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

    assert abjad.inspect(staff).wellformed()
    assert abjad.inspect(new).wellformed()


def test_Mutation_copy_03():
    """
    Three notes crossing measure boundaries.
    """

    staff = abjad.Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
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

    assert abjad.inspect(staff).wellformed()
    assert abjad.inspect(new).wellformed()


def test_Mutation_copy_04():

    staff = abjad.Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
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

    assert abjad.inspect(new_staff).wellformed()


def test_Mutation_copy_05():

    staff = abjad.Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
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

    assert abjad.inspect(staff).wellformed()
    assert abjad.inspect(new_staff).wellformed()


def test_Mutation_copy_06():

    staff = abjad.Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
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

    assert abjad.inspect(staff).wellformed()
    assert abjad.inspect(new_staff).wellformed()


def test_Mutation_copy_07():

    staff = abjad.Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
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

    assert abjad.inspect(staff).wellformed()
    assert abjad.inspect(new_staff).wellformed()


def test_Mutation_copy_08():
    """
    Copies hairpin.
    """

    staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    abjad.hairpin('< !', staff[:4])

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
    assert abjad.inspect(staff).wellformed()
