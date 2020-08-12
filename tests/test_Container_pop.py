import abjad


def test_Container_pop_01():
    """
    Containers pop leaves correctly.
    Popped leaves abjad.detach from parent.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.slur(voice[:])
    abjad.beam(voice[1:2], beam_lone_notes=True)

    assert abjad.lilypond(voice) == abjad.String.normalize(
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

    assert abjad.lilypond(voice) == abjad.String.normalize(
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

    assert abjad.wf.wellformed(result)
    assert abjad.lilypond(result) == "d'8\n[\n]"


def test_Container_pop_02():
    """
    Containers pop nested containers correctly.
    """

    staff = abjad.Staff("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
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
    ), print(abjad.lilypond(staff))

    sequential = staff.pop()

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'8
                [
                d'8
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)

    assert abjad.lilypond(sequential) == abjad.String.normalize(
        r"""
        {
            e'8
            f'8
            ]
        }
        """
    ), print(abjad.lilypond(sequential))

    assert abjad.wf.wellformed(sequential)
