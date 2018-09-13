import abjad


def test_Container__get_spanners_that_dominate_slice_01():
    """
    Get dominant spanners over zero-length slice.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:2])
    glissando = abjad.Glissando()
    abjad.attach(glissando, voice[:])

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \glissando
            d'8
            ]
            \glissando
            e'8
            \glissando
            f'8
        }
        """
        )

    receipt = voice._get_spanners_that_dominate_slice(2, 2)

    assert len(receipt) == 1
    assert (glissando, 2) in receipt
