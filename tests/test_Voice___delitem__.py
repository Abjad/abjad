import abjad


def test_Voice___delitem___01():
    """
    Delete container from voice.
    """

    voice = abjad.Voice(
        r"""
        c'8
        [
        \glissando
        {
            d'8
            \glissando
            e'8
            \glissando
        }
        f'8 ]
        """
    )

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \glissando
            {
                d'8
                \glissando
                e'8
                \glissando
            }
            f'8
            ]
        }
        """
    )

    container = voice[1]
    del voice[1:2]

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \glissando
            f'8
            ]
        }
        """
    )

    assert abjad.wf.wellformed(voice)
    assert abjad.wf.wellformed(container)
