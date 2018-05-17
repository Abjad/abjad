import abjad


def test_scoretools_Mutation_copy_01():
    """
    Deep copies components.
    Deep copies spanners that abjad.attach to client.
    Fractures spanners that abjad.attach to components not in client.
    Returns Python list of copied components.
    """

    voice = abjad.Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    leaves = abjad.select(voice).leaves()
    slur = abjad.Slur()
    abjad.attach(slur, leaves)
    trill = abjad.TrillSpanner()
    abjad.attach(trill, leaves)
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {   % measure
                \time 2/8
                c'8
                [
                (
                \startTrillSpan
                d'8
            }   % measure
            {   % measure
                e'8
                f'8
            }   % measure
            {   % measure
                g'8
                a'8
                ]
                )
                \stopTrillSpan
            }   % measure
        }
        """
        )

    result = abjad.mutate(leaves[2:4]).copy()
    new = abjad.Voice(result)

    assert format(new) == abjad.String.normalize(
        r"""
        \new Voice
        {
            e'8
            [
            (
            \startTrillSpan
            f'8
            ]
            )
            \stopTrillSpan
        }
        """
        )
    assert abjad.inspect(voice).is_well_formed()
    assert abjad.inspect(new).is_well_formed()


def test_scoretools_Mutation_copy_02():
    """
    Copy one measure and fracture spanners.
    """

    voice = abjad.Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    leaves = abjad.select(voice).leaves()
    slur = abjad.Slur()
    abjad.attach(slur, leaves)
    trill = abjad.TrillSpanner()
    abjad.attach(trill, leaves)
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {   % measure
                \time 2/8
                c'8
                [
                (
                \startTrillSpan
                d'8
            }   % measure
            {   % measure
                e'8
                f'8
            }   % measure
            {   % measure
                g'8
                a'8
                ]
                )
                \stopTrillSpan
            }   % measure
        }
        """
        )

    result = abjad.mutate(voice[1:2]).copy()
    new = abjad.Voice(result)

    assert format(new) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {   % measure
                \time 2/8
                e'8
                [
                (
                \startTrillSpan
                f'8
                ]
                )
                \stopTrillSpan
            }   % measure
        }
        """
        )
    assert abjad.inspect(voice).is_well_formed()
    assert abjad.inspect(new).is_well_formed()


def test_scoretools_Mutation_copy_03():
    """
    Three notes crossing measure boundaries.
    """

    voice = abjad.Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    leaves = abjad.select(voice).leaves()
    slur = abjad.Slur()
    abjad.attach(slur, leaves)
    trill = abjad.TrillSpanner()
    abjad.attach(trill, leaves)
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {   % measure
                \time 2/8
                c'8
                [
                (
                \startTrillSpan
                d'8
            }   % measure
            {   % measure
                e'8
                f'8
            }   % measure
            {   % measure
                g'8
                a'8
                ]
                )
                \stopTrillSpan
            }   % measure
        }
        """
        )

    result = abjad.mutate(leaves[-3:]).copy()
    new = abjad.Voice(result)

    assert format(new) == abjad.String.normalize(
        r"""
        \new Voice
        {
            f'8
            [
            (
            \startTrillSpan
            g'8
            a'8
            ]
            )
            \stopTrillSpan
        }
        """
        )
    assert abjad.inspect(voice).is_well_formed()
    assert abjad.inspect(new).is_well_formed()


def test_scoretools_Mutation_copy_04():

    voice = abjad.Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {   % measure
                \time 2/8
                c'8
                [
                (
                d'8
            }   % measure
            {   % measure
                e'8
                f'8
            }   % measure
            {   % measure
                g'8
                a'8
            }   % measure
            {   % measure
                b'8
                c''8
                ]
                )
            }   % measure
        }
        """
        )

    selection = abjad.select(voice)
    new_selection = abjad.mutate(selection).copy()
    new_voice = new_selection[0]
    for component in abjad.iterate(new_voice).components():
        abjad.detach(abjad.Spanner, component)

    assert format(new_voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {   % measure
                \time 2/8
                c'8
                d'8
            }   % measure
            {   % measure
                e'8
                f'8
            }   % measure
            {   % measure
                g'8
                a'8
            }   % measure
            {   % measure
                b'8
                c''8
            }   % measure
        }
        """
        )
    assert abjad.inspect(new_voice).is_well_formed()


def test_scoretools_Mutation_copy_05():

    voice = abjad.Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {   % measure
                \time 2/8
                c'8
                [
                (
                d'8
            }   % measure
            {   % measure
                e'8
                f'8
            }   % measure
            {   % measure
                g'8
                a'8
            }   % measure
            {   % measure
                b'8
                c''8
                ]
                )
            }   % measure
        }
        """
        )

    result = abjad.mutate(voice[1:]).copy()
    new_voice = abjad.Voice(result)
    for component in abjad.iterate(new_voice).components():
        abjad.detach(abjad.Spanner, component)

    assert format(new_voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {   % measure
                \time 2/8
                e'8
                f'8
            }   % measure
            {   % measure
                g'8
                a'8
            }   % measure
            {   % measure
                b'8
                c''8
            }   % measure
        }
        """
        )
    assert abjad.inspect(voice).is_well_formed()
    assert abjad.inspect(new_voice).is_well_formed()


def test_scoretools_Mutation_copy_06():

    voice = abjad.Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {   % measure
                \time 2/8
                c'8
                [
                (
                d'8
            }   % measure
            {   % measure
                e'8
                f'8
            }   % measure
            {   % measure
                g'8
                a'8
            }   % measure
            {   % measure
                b'8
                c''8
                ]
                )
            }   % measure
        }
        """
        )

    result = abjad.mutate(leaves[:6]).copy()
    new_voice = abjad.Voice(result)
    for component in abjad.iterate(new_voice).components():
        abjad.detach(abjad.Spanner, component)

    assert format(new_voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
        """
        )
    assert abjad.inspect(voice).is_well_formed()
    assert abjad.inspect(new_voice).is_well_formed()


def test_scoretools_Mutation_copy_07():

    voice = abjad.Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {   % measure
                \time 2/8
                c'8
                [
                (
                d'8
            }   % measure
            {   % measure
                e'8
                f'8
            }   % measure
            {   % measure
                g'8
                a'8
            }   % measure
            {   % measure
                b'8
                c''8
                ]
                )
            }   % measure
        }
        """
        )

    result = abjad.mutate(voice[-2:]).copy()
    new_voice = abjad.Voice(result)
    for component in abjad.iterate(new_voice).components():
        abjad.detach(abjad.Spanner, component)

    assert format(new_voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {   % measure
                \time 2/8
                g'8
                a'8
            }   % measure
            {   % measure
                b'8
                c''8
            }   % measure
        }
        """
        )

    assert abjad.inspect(voice).is_well_formed()
    assert abjad.inspect(new_voice).is_well_formed()


def test_scoretools_Mutation_copy_08():
    """
    Copies hairpin.
    """

    staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    crescendo = abjad.Hairpin('<')
    abjad.attach(crescendo, staff[:4])

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
    assert abjad.inspect(staff).is_well_formed()
