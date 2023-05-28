import abjad


def test_Container_pop_01():
    """
    Containers pop leaves correctly.
    Popped leaves abjad.detach from parent.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.slur(voice[:])
    abjad.beam(voice[1:2], beam_lone_notes=True)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            (
            d'8
            [
            ]
            e'8
            f'8
            )
        }
        """
    ), print(abjad.lilypond(voice))

    result = voice.pop(1)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            (
            e'8
            f'8
            )
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)

    "Result is now d'8 [ ]"

    assert abjad.lilypond(result) == "d'8\n[\n]"
    assert abjad.wf.wellformed(result, check_beamed_lone_notes=False)


def test_Container_pop_02():
    """
    Containers pop nested containers correctly.
    """

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select.leaves(voice)
    abjad.beam(leaves)

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
            {
                e'8
                f'8
                ]
            }
        }
        """
    ), print(abjad.lilypond(voice))

    sequential = voice.pop()

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)

    assert abjad.lilypond(sequential) == abjad.string.normalize(
        r"""
        {
            e'8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(sequential))

    assert abjad.wf.wellformed(sequential)
