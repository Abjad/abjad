import copy

import abjad


def test_Container___copy___01():
    """
    Containers copy simultaneity flag.
    """

    container_1 = abjad.Container([abjad.Voice("c'8 d'8"), abjad.Voice("c''8 b'8")])
    container_1.simultaneous = True
    container_2 = copy.copy(container_1)

    assert abjad.lilypond(container_1) == abjad.string.normalize(
        r"""
        <<
            \new Voice
            {
                c'8
                d'8
            }
            \new Voice
            {
                c''8
                b'8
            }
        >>
        """
    )

    assert abjad.lilypond(container_2) == abjad.string.normalize(
        r"""
        <<
        >>
        """
    )

    assert container_1 is not container_2
