import abjad


def test_Beam_detach_01():
    """
    Detach length-one spanner.
    """

    staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beam = abjad.Beam(beam_lone_notes=True)
    abjad.attach(beam, staff[:1])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            ]
            cs'8
            d'8
            ef'8
            e'8
            f'8
            fs'8
            g'8
        }
        """
        )

    abjad.detach(beam, staff[0])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            cs'8
            d'8
            ef'8
            e'8
            f'8
            fs'8
            g'8
        }
        """
        )

    assert abjad.inspect(staff).is_well_formed()


def test_Beam_detach_02():
    """
    Detach length-four spanner.
    """

    staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beam = abjad.Beam()
    abjad.attach(beam, staff[:4])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            cs'8
            d'8
            ef'8
            ]
            e'8
            f'8
            fs'8
            g'8
        }
        """
        )

    abjad.detach(beam, staff[0])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            cs'8
            d'8
            ef'8
            e'8
            f'8
            fs'8
            g'8
        }
        """
        )

    assert abjad.inspect(staff).is_well_formed()
