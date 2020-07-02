import abjad


def test_Container___delitem___01():
    """
    Deletes in-score container.
    """

    voice = abjad.Voice("{ c'8 ( d'8 ) } { e'8 ( f'8 ) }")
    leaves = abjad.select(voice).leaves()
    abjad.beam(leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                (
                [
                d'8
                )
            }
            {
                e'8
                (
                f'8
                )
                ]
            }
        }
        """
    )

    container = voice[0]
    del voice[0]

    # container no longer appears in score
    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                e'8
                (
                f'8
                )
                ]
            }
        }
        """
    ), print(format(voice))

    assert abjad.wellformed(voice)

    # container leaves are still slurred
    assert format(container) == abjad.String.normalize(
        r"""
        {
            c'8
            (
            [
            d'8
            )
        }
        """
    ), print(format(container))

    assert abjad.wellformed(container)


def test_Container___delitem___02():
    """
    Deletes in-score leaf.
    """

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del voice[1]

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            e'8
            f'8
            ]
        }
        """
    )

    assert abjad.wellformed(voice)


def test_Container___delitem___03():
    """
    Deletes slice in middle of container.
    """

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del voice[1:3]

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            f'8
            ]
        }
        """
    )

    assert abjad.wellformed(voice)


def test_Container___delitem___04():
    """
    Delete slice at beginning of container.
    """

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del voice[:2]

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            e'8
            f'8
            ]
        }
        """
    )

    assert abjad.wellformed(voice)


def test_Container___delitem___05():
    """
    Deletes slice at end of container.
    """

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del voice[2:]

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
        }
        """
    )

    assert abjad.wellformed(voice)


def test_Container___delitem___06():
    """
    Deletes container contents.
    """

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del voice[:]

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
        }
        """
    )

    assert not len(voice)


def test_Container___delitem___07():
    """
    Deletes leaf from tuplet.
    """

    tuplet = abjad.Tuplet(abjad.Multiplier((2, 3)), "c'8 [ d'8 e'8 ]")
    del tuplet[1]

    assert format(tuplet) == abjad.String.normalize(
        r"""
        \tweak edge-height #'(0.7 . 0)
        \times 2/3 {
            c'8
            [
            e'8
            ]
        }
        """
    )

    assert abjad.wellformed(tuplet)


def test_Container___delitem___08():
    """
    Deletes leaf from nested container.
    """

    voice = abjad.Voice("c'8 [ { d'8 e'8 } f'8 ]")
    leaves = abjad.select(voice).leaves()
    abjad.glissando(leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \glissando %! abjad.glissando(7)
            {
                d'8
                \glissando %! abjad.glissando(7)
                e'8
                \glissando %! abjad.glissando(7)
            }
            f'8
            ]
        }
        """
    ), abjad.f(voice)

    leaf = leaves[1]
    del voice[1][0]

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \glissando %! abjad.glissando(7)
            {
                e'8
                \glissando %! abjad.glissando(7)
            }
            f'8
            ]
        }
        """
    ), abjad.f(voice)

    assert abjad.wellformed(voice)
    assert abjad.wellformed(leaf)
