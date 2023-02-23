import abjad


def test_mutate__are_contiguous_logical_voice_01():
    """
    Components that start at the same moment are bad.
    Even if components are all part of the same logical voice.
    """

    voice = abjad.Voice(
        r"""
        {
            c'8
            d'8
        }
        \new Voice {
            e'8
            f'8
        }
        {
            g'8
            a'8
        }
        """
    )

    voices = [voice, voice[0]]
    assert not abjad.mutate._are_contiguous_logical_voice(voices)
    voices = list(voice[0:1]) + list(voice[0])
    assert not abjad.mutate._are_contiguous_logical_voice(voices)
    voices = list(voice[-1:]) + list(voice[-1])
    assert not abjad.mutate._are_contiguous_logical_voice(voices)


def test_mutate__are_contiguous_logical_voice_02():
    """
    Is true for strictly contiguous leaves in same staff.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    assert abjad.mutate._are_contiguous_logical_voice(staff[:])


def test_mutate__are_contiguous_logical_voice_03():
    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
    ]
    assert abjad.mutate._are_contiguous_logical_voice(notes)


def test_mutate__are_contiguous_logical_voice_04():
    """
    Is false for time-reordered leaves in staff.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    leaves = list(staff[2:]) + list(staff[:2])
    assert not abjad.mutate._are_contiguous_logical_voice(leaves)


def test_mutate__are_contiguous_logical_voice_05():
    """
    Is true for unincorporated component.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    assert abjad.mutate._are_contiguous_logical_voice([staff])


def test_mutate__are_contiguous_logical_voice_06():
    """
    Is true for empty input.
    """

    assert abjad.mutate._are_contiguous_logical_voice([])


def test_mutate__are_contiguous_logical_voice_07():
    """
    False when components belonging to same logical voice are ommitted.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8 g'8 a'8")
    abjad.beam(voice[:])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            f'8
            g'8
            a'8
            ]
        }
        """
    )

    leaves = list(voice[:2]) + list(voice[-2:])
    assert not abjad.mutate._are_contiguous_logical_voice(leaves)


def test_mutate__are_contiguous_logical_voice_08():
    """
    False when components belonging to same logical voice are ommitted.
    """

    voice = abjad.Voice(
        r"""
        {
            c'8
            [
            d'8
        }
        {
            e'8
            f'8
        }
        {
            g'8
            a'8
            ]
        }
        """
    )

    components = list(voice[:1]) + list(voice[-1:])
    assert not abjad.mutate._are_contiguous_logical_voice(components)
