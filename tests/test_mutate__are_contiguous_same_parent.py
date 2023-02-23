import abjad


def test_mutate__are_contiguous_same_parent_01():
    """
    Is true for strictly contiguous leaves in voice.
    Is false for other time orderings of leaves in voice.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")

    assert abjad.mutate._are_contiguous_same_parent(voice[:])

    other = list(reversed(voice[:]))
    assert not abjad.mutate._are_contiguous_same_parent(other)

    components = []
    components.extend(voice[2:])
    components.extend(voice[:2])
    assert not abjad.mutate._are_contiguous_same_parent(components)

    components = []
    components.extend(voice[3:4])
    components.extend(voice[:1])
    assert not abjad.mutate._are_contiguous_same_parent(components)
    components = [voice]
    components.extend(voice[:])
    assert not abjad.mutate._are_contiguous_same_parent(components)


def test_mutate__are_contiguous_same_parent_02():
    """
    Is true for unincorporated components when orphans allowed.
    Is false for unincorporated components when orphans not allowed.
    """

    voice = abjad.Voice(
        r"""
        {
            c'8
            d'8
        }
        {
            e'8
            f'8
        }
        """
    )

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }
        """
    )

    assert abjad.mutate._are_contiguous_same_parent([voice])

    assert abjad.mutate._are_contiguous_same_parent(voice[:])

    assert abjad.mutate._are_contiguous_same_parent(voice[0][:])
    assert abjad.mutate._are_contiguous_same_parent(voice[1][:])

    leaves = abjad.select.leaves(voice)
    assert not abjad.mutate._are_contiguous_same_parent(leaves)


def test_mutate__are_contiguous_same_parent_03():
    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
    ]

    assert abjad.mutate._are_contiguous_same_parent(notes)


def test_mutate__are_contiguous_same_parent_04():
    """
    Empty selection returns true.
    """

    assert abjad.mutate._are_contiguous_same_parent([])
