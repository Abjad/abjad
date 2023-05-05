import abjad


def test_mutate__split_container_by_duration_01():
    """
    Split one container in score.
    Adds tie after split.
    """

    voice = abjad.Voice()
    voice.append(abjad.Container("c'8 d'8"))
    voice.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
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
    ), print(abjad.lilypond(voice))

    abjad.mutate._split_container_by_duration(voice[0], abjad.Duration(1, 32))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'32
                [
                (
                ~
            }
            {
                c'16.
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
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__split_container_by_duration_02():
    """
    Split in-score container at split offset with non-power-of-two denominator.
    """

    voice = abjad.Voice()
    voice.append(abjad.Container("c'8 d'8"))
    voice.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
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
    ), print(abjad.lilypond(voice))

    abjad.mutate._split_container_by_duration(voice[0], abjad.Duration(1, 5))

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                (
                \tweak edge-height #'(0.7 . 0)
                \times 4/5
                {
                    d'16.
                    ~
                }
            }
            {
                \tweak edge-height #'(0.7 . 0)
                \times 4/5
                {
                    d'16
                    ]
                }
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
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)
