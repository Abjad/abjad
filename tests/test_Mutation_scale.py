import abjad


def test_Mutation_scale_01():
    """
    Scales leaves by dot-generating multiplier.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.mutate(voice).scale(abjad.Multiplier(3, 2))

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8.
            d'8.
            e'8.
            f'8.
        }
        """
    )

    assert abjad.inspect(voice).wellformed()


def test_Mutation_scale_02():
    """
    Scales leaves by tie-generating multiplier.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.mutate(voice).scale(abjad.Multiplier(5, 4))

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            ~
            c'32
            d'8
            ~
            d'32
            e'8
            ~
            e'32
            f'8
            ~
            f'32
        }
        """
    )

    assert abjad.inspect(voice).wellformed()


def test_Mutation_scale_03():
    """
    Scales leaves by tuplet-generating multiplier.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.mutate(voice).scale(abjad.Multiplier(4, 3))

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'4
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'4
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                e'4
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                f'4
            }
        }
        """
    )

    assert abjad.inspect(voice).wellformed()


def test_Mutation_scale_04():
    """
    Scales leaves by tie- and tuplet-generating multiplier.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.mutate(voice).scale(abjad.Multiplier(5, 6))

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8
                ~
                c'32
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'8
                ~
                d'32
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                e'8
                ~
                e'32
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                f'8
                ~
                f'32
            }
        }
        """
    ), print(format(voice))

    assert abjad.inspect(voice).wellformed()


def test_Mutation_scale_05():
    """
    Undo scale of 5/4 with scale of 4/5.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.mutate(voice).scale(abjad.Multiplier(5, 4))

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            ~
            c'32
            d'8
            ~
            d'32
            e'8
            ~
            e'32
            f'8
            ~
            f'32
        }
        """
    )

    abjad.mutate(voice).scale(abjad.Multiplier(4, 5))

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    assert abjad.inspect(voice).wellformed()
