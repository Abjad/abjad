import abjad


def test_Selection_are_contiguous_logical_voice_01():
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

    selection = abjad.select([voice, voice[0]])
    assert not selection.are_contiguous_logical_voice()
    selection = voice[0:1] + voice[0][:]
    assert not selection.are_contiguous_logical_voice()
    selection = voice[-1:] + voice[-1][:]
    assert not selection.are_contiguous_logical_voice()


def test_Selection_are_contiguous_logical_voice_02():
    """
    Is true for strictly contiguous leaves in same staff.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    assert staff[:].are_contiguous_logical_voice()


def test_Selection_are_contiguous_logical_voice_03():

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
    ]
    assert abjad.select(notes).are_contiguous_logical_voice()


def test_Selection_are_contiguous_logical_voice_04():
    """
    Is false for time-reordered leaves in staff.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    selection = staff[2:] + staff[:2]
    assert not selection.are_contiguous_logical_voice()


def test_Selection_are_contiguous_logical_voice_05():
    """
    Is true for unincorporated component.
    """

    abjad.select(abjad.Staff("c'8 d'8 e'8 f'8")).are_contiguous_logical_voice()


def test_Selection_are_contiguous_logical_voice_06():
    """
    Is true for empty selection.
    """

    assert abjad.Selection().are_contiguous_logical_voice()


def test_Selection_are_contiguous_logical_voice_07():
    """
    False when components belonging to same logical voice are ommitted.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8 g'8 a'8")
    abjad.beam(voice[:])

    assert format(voice) == abjad.String.normalize(
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

    selection = voice[:2] + voice[-2:]
    assert not selection.are_contiguous_logical_voice()


def test_Selection_are_contiguous_logical_voice_08():
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

    selection = voice[:1] + voice[-1:]
    assert not selection.are_contiguous_logical_voice()
