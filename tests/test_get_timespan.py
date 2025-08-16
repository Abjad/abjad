import pytest

import abjad


def test_get_timespan_01():
    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    for i, x in enumerate(voice):
        assert abjad.get.timespan(x).start_offset == abjad.duration.offset(i, 8)


def test_get_timespan_02():
    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    for i, x in enumerate(staff):
        assert abjad.get.timespan(x).start_offset == abjad.duration.offset(i, 8)


def test_get_timespan_03():
    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    staff[-1] = abjad.Rest("r8")
    for i, x in enumerate(staff):
        assert abjad.get.timespan(x).start_offset == abjad.duration.offset(i, 8)


def test_get_timespan_04():
    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    staff[10:10] = [abjad.Rest("r8")]
    for i, x in enumerate(staff):
        assert abjad.get.timespan(x).start_offset == abjad.duration.offset(i, 8)


def test_get_timespan_05():
    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    staff[10:12] = [abjad.Rest("r8")]
    for i, x in enumerate(staff):
        assert abjad.get.timespan(x).start_offset == abjad.duration.offset(i, 8)


def test_get_timespan_06():
    """
    Offset works with voices.
    """

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_1.set_name("voice")
    voice_2.set_name("voice")
    container = abjad.Container([voice_1, voice_2])
    leaves = abjad.select.leaves(container)
    for i, x in enumerate(leaves):
        assert abjad.get.timespan(x).start_offset == abjad.duration.offset(i, 8)


def test_get_timespan_07():
    tuplet = abjad.Tuplet("3:2", "c'8 c'8 c'8")
    for i, x in enumerate(tuplet):
        assert abjad.get.timespan(x).start_offset == abjad.duration.offset(i, 12)


def test_get_timespan_08():
    tuplet_1 = abjad.Tuplet("3:2", "c'8 c'8 c'8")
    voice = abjad.Voice([abjad.Note("c'8"), tuplet_1, abjad.Note("c'8")])
    offset = abjad.duration.offset(0)
    pairs = [(1, 8), (1, 12), (1, 12), (1, 12), (1, 8)]
    durations = abjad.duration.durations(pairs)
    leaves = abjad.select.leaves(voice)
    for leaf, duration in zip(leaves, durations, strict=True):
        assert abjad.get.timespan(leaf).start_offset == offset
        offset += duration


def test_get_timespan_09():
    """
    Offset works on nested tuplets.
    """

    tuplet_1 = abjad.Tuplet("3:2", "c'8 c'8 c'8")
    tuplet = abjad.Tuplet("3:2", [abjad.Note("c'4"), tuplet_1, abjad.Note("c'4")])
    offset = abjad.duration.offset(0)
    pairs = [(1, 6), (1, 18), (1, 18), (1, 18), (1, 6)]
    durations = abjad.duration.durations(pairs)
    leaves = abjad.select.leaves(tuplet)
    for leaf, duration in zip(leaves, durations):
        assert abjad.get.timespan(leaf).start_offset == offset
        offset += duration


def test_get_timespan_10():
    """
    Offset works with simultaneous structures.
    """

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([voice_1, voice_2])
    staff.set_simultaneous(True)
    for i, leaf in enumerate(voice_1):
        start_offset = abjad.get.timespan(leaf).start_offset
        assert start_offset == abjad.duration.offset(i, 8)
    for i, leaf in enumerate(voice_2):
        start_offset = abjad.get.timespan(leaf).start_offset
        assert start_offset == abjad.duration.offset(i, 8)


def test_get_timespan_11():
    """
    Offset on leaves works in nested contexts.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([abjad.Note("c'8"), voice, abjad.Note("c'8")])
    leaves = abjad.select.leaves(staff)
    for i, leaf in enumerate(leaves):
        start_offset = abjad.get.timespan(leaf).start_offset
        assert start_offset == abjad.duration.offset(i, 8)
    leaves = abjad.select.leaves(voice)
    for i, leaf in enumerate(leaves):
        start_offset = abjad.get.timespan(leaf).start_offset
        assert start_offset == abjad.duration.offset(i, 8) + abjad.Duration(1, 8)


def test_get_timespan_12():
    """
    Offset on leaves works in sequential contexts.
    """

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.Staff([voice_1, voice_2])
    for i, leaf in enumerate(voice_1):
        start_offset = abjad.get.timespan(leaf).start_offset
        assert start_offset == abjad.duration.offset(i, 8)
    for i, leaf in enumerate(voice_2):
        start_offset = abjad.get.timespan(leaf).start_offset
        assert start_offset == abjad.duration.offset(i, 8) + abjad.Duration(1, 2)


def test_get_timespan_13():
    """
    Offset on leaves works in nested simultaneous contexts.
    """

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([voice_1, voice_2])
    staff.set_simultaneous(True)
    for i, leaf in enumerate(voice_1):
        start_offset = abjad.get.timespan(leaf).start_offset
        assert start_offset == abjad.duration.offset(i, 8)
    for i, leaf in enumerate(voice_2):
        start_offset = abjad.get.timespan(leaf).start_offset
        assert start_offset == abjad.duration.offset(i, 8)


def test_get_timespan_14():
    """
    Offset on leaves works in nested simultaneous and sequential contexts.
    """

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_3 = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([abjad.Container([voice_1, voice_2]), voice_3])
    staff[0].set_simultaneous(True)
    for i, leaf in enumerate(voice_3):
        start_offset = abjad.get.timespan(leaf).start_offset
        assert start_offset == abjad.duration.offset(i, 8) + abjad.Duration(1, 2)


def test_get_timespan_15():
    """
    Offset on leaves works in nested simultaneous and sequential contexts.
    """

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_3 = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([voice_3, abjad.Container([voice_1, voice_2])])
    staff[1].set_simultaneous(True)
    for i, leaf in enumerate(voice_1):
        start_offset = abjad.get.timespan(leaf).start_offset
        assert start_offset == abjad.duration.offset(i, 8) + abjad.Duration(1, 2)
    for i, leaf in enumerate(voice_2):
        start_offset = abjad.get.timespan(leaf).start_offset
        assert start_offset == abjad.duration.offset(i, 8) + abjad.Duration(1, 2)


def test_get_timespan_16():
    """
    Offsets works on sequential voices.
    """

    staff = abjad.Staff(
        [abjad.Voice("c'8 d'8 e'8 f'8"), abjad.Voice("c'8 d'8 e'8 f'8")]
    )
    staff[0].set_name("voice")
    staff[1].set_name("voice")
    for i, voice in enumerate(staff):
        start_offset = abjad.get.timespan(voice).start_offset
        assert start_offset == abjad.duration.offset(4 * i, 8)


def test_get_timespan_17():
    """
    Prolated offset does NOT go across sequential staves.
    """

    container = abjad.Container(
        [abjad.Staff("c'8 d'8 e'8 f'8"), abjad.Staff("c'8 d'8 e'8 f'8")]
    )
    container[0].set_name("staff")
    container[1].set_name("staff")
    start_offset = abjad.get.timespan(container[0]).start_offset
    assert start_offset == abjad.duration.offset(0)
    start_offset = abjad.get.timespan(container[1]).start_offset
    assert start_offset == abjad.duration.offset(1, 2)


def test_get_timespan_18():
    """
    Offsets works with nested voices.
    """

    staff = abjad.Staff(
        [abjad.Voice("c'8 d'8 e'8 f'8"), abjad.Voice("c'8 d'8 e'8 f'8")]
    )
    for i, voice in enumerate(staff):
        start_offset = abjad.get.timespan(voice).start_offset
        assert start_offset == abjad.duration.offset(4 * i, 8)


def test_get_timespan_19():
    """
    Offsets works on sequential tuplets.
    """

    voice = abjad.Voice(
        [
            abjad.Tuplet("3:2", "c'8 d'8 e'8"),
            abjad.Tuplet("3:2", "c'8 d'8 e'8"),
            abjad.Tuplet("3:2", "c'8 d'8 e'8"),
        ]
    )
    assert abjad.get.timespan(voice[0]).start_offset == abjad.duration.offset(0, 4)
    assert abjad.get.timespan(voice[1]).start_offset == abjad.duration.offset(1, 4)
    assert abjad.get.timespan(voice[2]).start_offset == abjad.duration.offset(2, 4)


def test_get_timespan_20():
    """
    Offsets work on tuplets between notes.
    """

    tuplet_1 = abjad.Tuplet("3:2", "c'8 c'8 c'8")
    voice = abjad.Voice([abjad.Note("c'8"), tuplet_1, abjad.Note("c'8")])
    assert abjad.get.timespan(voice[0]).start_offset == abjad.duration.offset(0, 8)
    assert abjad.get.timespan(voice[1]).start_offset == abjad.duration.offset(1, 8)
    assert abjad.get.timespan(voice[2]).start_offset == abjad.duration.offset(3, 8)


def test_get_timespan_21():
    """
    Offsets work on nested tuplets.
    """

    tuplet_1 = abjad.Tuplet("2:1", "c'8 d'8 e'8 f'8")
    contents = [abjad.Note("c'4"), tuplet_1, abjad.Note("c'4")]
    tuplet = abjad.Tuplet("3:2", contents)
    assert abjad.get.timespan(tuplet[0]).start_offset == abjad.duration.offset(0, 6)
    assert abjad.get.timespan(tuplet[1]).start_offset == abjad.duration.offset(1, 6)
    assert abjad.get.timespan(tuplet[2]).start_offset == abjad.duration.offset(2, 6)


def test_get_timespan_22():
    """
    Offsets work on nested contexts.
    """

    inner_voice = abjad.Voice("c'8 d'8 e'8 f'8", name="voice")
    outer_voice = abjad.Voice([abjad.Note("c'8"), inner_voice], name="voice")
    abjad.Staff([abjad.Note("cs'8"), outer_voice])
    assert abjad.get.timespan(inner_voice).start_offset == abjad.duration.offset(2, 8)
    assert abjad.get.timespan(outer_voice).start_offset == abjad.duration.offset(1, 8)


def test_get_timespan_23():
    """
    Offsets work on nested simultaneous contexts.
    """

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([voice_1, voice_2])
    staff.set_simultaneous(True)
    assert abjad.get.timespan(staff[0]).start_offset == abjad.duration.offset(0)
    assert abjad.get.timespan(staff[1]).start_offset == abjad.duration.offset(0)


def test_get_timespan_24():
    """
    Offsets works in nested simultaneous and sequential contexts.
    """

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_1b = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2b = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_1.set_name("voiceOne")
    voice_1b.set_name("voiceOne")
    staff_1 = abjad.Staff([voice_1, voice_1b])
    staff_2 = abjad.Staff([voice_2, voice_2b])
    abjad.StaffGroup([staff_1, staff_2])
    assert abjad.get.timespan(voice_1).start_offset == abjad.duration.offset(0)
    assert abjad.get.timespan(voice_2).start_offset == abjad.duration.offset(0)
    assert abjad.get.timespan(voice_1b).start_offset == abjad.duration.offset(4, 8)
    assert abjad.get.timespan(voice_2b).start_offset == abjad.duration.offset(4, 8)


def test_get_timespan_25():
    """
    Offset seconds can not calculate without excplit metronome mark.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")

    with pytest.raises(Exception):
        abjad.get.timespan(staff[0], in_seconds=True).start_offset


def test_get_timespan_26():
    """
    Offset seconds work with explicit metronome mark.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    mark = abjad.MetronomeMark(abjad.Duration(1, 8), 48)
    abjad.attach(mark, staff[0], context="Staff")

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \tempo 8=48
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    start_offset = abjad.get.timespan(staff[0], in_seconds=True).start_offset
    assert start_offset == abjad.duration.offset(0)
    start_offset = abjad.get.timespan(staff[1], in_seconds=True).start_offset
    assert start_offset == abjad.duration.offset(5, 4)


def test_Tuplet_timespan_01():
    staff = abjad.Staff(r"c'4 d'4 \tuplet 3/2 { e'4 f'4 g'4 }")

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            \tuplet 3/2
            {
                e'4
                f'4
                g'4
            }
        }
        """
    )

    assert abjad.get.timespan(staff) == abjad.Timespan(
        abjad.duration.offset(0), abjad.duration.offset(1)
    )
    assert abjad.get.timespan(staff[0]) == abjad.Timespan(
        abjad.duration.offset(0), abjad.duration.offset(1, 4)
    )
    assert abjad.get.timespan(staff[1]) == abjad.Timespan(
        abjad.duration.offset(1, 4), abjad.duration.offset(1, 2)
    )
    assert abjad.get.timespan(staff[-1]) == abjad.Timespan(
        abjad.duration.offset(1, 2), abjad.duration.offset(1)
    )


def test_Tuplet_timespan_02():
    staff = abjad.Staff(r"c'4 d'4 \tuplet 3/2 { e'4 f'4 g'4 }")
    leaves = abjad.select.leaves(staff)
    score = abjad.Score([staff])
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
    abjad.attach(mark, leaves[0])

    assert abjad.lilypond(score) == abjad.string.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \tempo 4=60
                c'4
                d'4
                \tuplet 3/2
                {
                    e'4
                    f'4
                    g'4
                }
            }
        >>
        """
    )

    assert abjad.get.timespan(staff, in_seconds=True) == abjad.Timespan(
        abjad.duration.offset(0), abjad.duration.offset(4)
    )
    assert abjad.get.timespan(staff[0], in_seconds=True) == abjad.Timespan(
        abjad.duration.offset(0), abjad.duration.offset(1)
    )
    assert abjad.get.timespan(staff[1], in_seconds=True) == abjad.Timespan(
        abjad.duration.offset(1), abjad.duration.offset(2)
    )
    assert abjad.get.timespan(staff[-1], in_seconds=True) == abjad.Timespan(
        abjad.duration.offset(2), abjad.duration.offset(4)
    )
