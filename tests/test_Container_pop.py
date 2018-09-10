import abjad


def test_Container_pop_01():
    """
    Containers pop leaves correctly.
    Popped leaves abjad.detach from parent.
    Popped leaves withdraw from crossing spanners.
    Popped leaves carry covered spanners forward.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.slur(voice[:])
    abjad.beam(voice[1:2], beam_lone_notes=True)

    assert format(voice) == abjad.String.normalize(
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
        ), print(format(voice))

    result = voice.pop(1)

    assert format(voice) == abjad.String.normalize(
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
        ), print(format(voice))

    assert abjad.inspect(voice).wellformed()

    "Result is now d'8 [ ]"

    assert abjad.inspect(result).wellformed()
    assert format(result) == "d'8\n[\n]"


def test_Container_pop_02():
    """
    Containers pop nested containers correctly.
    Popped containers abjad.detach from both parent and spanners.
    """

    staff = abjad.Staff("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves)

    assert format(staff) == abjad.String.normalize(
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
        ), print(format(staff))

    sequential = staff.pop()

    assert format(staff) == abjad.String.normalize(
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
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()

    assert format(sequential) == abjad.String.normalize(
        r"""
        {
            e'8
            f'8
            ]
        }
        """
        ), print(format(sequential))

    assert abjad.inspect(sequential).wellformed()
