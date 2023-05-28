import pytest

import abjad


def test_get_bar_line_crossing_01():
    """
    Works with partial.
    """

    staff = abjad.Staff("c'8 d'8 e'4 f'8")
    abjad.Score([staff], name="Score")
    time_signature = abjad.TimeSignature((2, 8), partial=abjad.Duration(1, 8))
    abjad.attach(time_signature, staff[0])

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \partial 8
            \time 2/8
            c'8
            d'8
            e'4
            f'8
        }
        """
    )

    assert not abjad.get.bar_line_crossing(staff[0])
    assert not abjad.get.bar_line_crossing(staff[1])
    assert abjad.get.bar_line_crossing(staff[2])
    assert not abjad.get.bar_line_crossing(staff[3])


def test_get_bar_line_crossing_02():
    """
    Works when no explicit time signature is abjad.attached.
    """

    staff = abjad.Staff("c'2 d'1 e'2")

    assert not abjad.get.bar_line_crossing(staff[0])
    assert abjad.get.bar_line_crossing(staff[1])
    assert not abjad.get.bar_line_crossing(staff[2])


def test_get_duration_01():
    """
    Container duration in seconds equals sum of leaf durations in seconds.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    score = abjad.Score([staff])
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 38)
    abjad.attach(mark, staff[0])
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 42)
    abjad.attach(mark, staff[2])

    assert abjad.lilypond(score) == abjad.string.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \tempo 4=38
                c'8
                d'8
                \tempo 4=42
                e'8
                f'8
            }
        >>
        """
    )

    assert abjad.get.duration(score, in_seconds=True) == abjad.Duration(400, 133)


def test_get_duration_02():
    """
    Container can not calculate duration in seconds without metronome mark.
    """

    container = abjad.Container("c'8 d'8 e'8 f'8")
    with pytest.raises(Exception):
        abjad.get.duration(container, in_seconds=True)


def test_get_duration_03():
    """
    Clock duration equals duration divide by effective tempo.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.Score([staff])
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 38)
    abjad.attach(mark, staff[0])
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 42)
    abjad.attach(mark, staff[2])

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \tempo 4=38
            c'8
            d'8
            \tempo 4=42
            e'8
            f'8
        }
        """
    )

    assert abjad.get.duration(staff[0], in_seconds=True) == abjad.Duration(15, 19)
    assert abjad.get.duration(staff[1], in_seconds=True) == abjad.Duration(15, 19)
    assert abjad.get.duration(staff[2], in_seconds=True) == abjad.Duration(5, 7)
    assert abjad.get.duration(staff[3], in_seconds=True) == abjad.Duration(5, 7)


def test_get_duration_04():
    """
    Clock duration can not calculate without metronome mark.
    """

    note = abjad.Note("c'4")
    with pytest.raises(Exception):
        abjad.get.duration(note, in_seconds=True)


def test_get_has_effective_indicator_01():
    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.attach("foo", staff[2], context="Staff")

    assert not abjad.get.has_effective_indicator(staff, str)
    assert not abjad.get.has_effective_indicator(staff[0], str)
    assert not abjad.get.has_effective_indicator(staff[1], str)
    assert abjad.get.has_effective_indicator(staff[2], str)
    assert abjad.get.has_effective_indicator(staff[3], str)


def test_get_has_indicator_01():
    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.attach("foo", staff[0])

    assert not abjad.get.has_indicator(staff, str)
    assert abjad.get.has_indicator(staff[0], str)
    assert not abjad.get.has_indicator(staff[1], str)
    assert not abjad.get.has_indicator(staff[2], str)
    assert not abjad.get.has_indicator(staff[3], str)


def test_get_has_indicator_02():
    staff = abjad.Staff("c'2 d'2")
    articulation = abjad.Articulation("staccato")
    abjad.attach(articulation, staff[0])

    assert abjad.get.has_indicator(staff[0], abjad.Articulation)
    assert not abjad.get.has_indicator(staff[1], abjad.Duration)


def test_get_has_indicator_03():
    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    command = abjad.LilyPondLiteral(r"\break", site="after")
    abjad.attach(command, staff[-1])

    assert not abjad.get.has_indicator(staff[0], abjad.LilyPondLiteral)
    assert not abjad.get.has_indicator(staff[1], abjad.LilyPondLiteral)
    assert not abjad.get.has_indicator(staff[2], abjad.LilyPondLiteral)
    assert abjad.get.has_indicator(staff[3], abjad.LilyPondLiteral)


def test_get_has_indicator_04():
    staff = abjad.Staff("c'2 d'2")
    stem_tremolo = abjad.StemTremolo(16)
    abjad.attach(stem_tremolo, staff[0])

    assert abjad.get.has_indicator(staff[0], abjad.StemTremolo)
    assert not abjad.get.has_indicator(staff[1], abjad.StemTremolo)


def test_get_has_indicator_05():
    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.Score([staff], name="Score")
    time_signature = abjad.TimeSignature((4, 8))
    abjad.attach(time_signature, staff[0])

    assert abjad.get.has_indicator(staff[0], abjad.TimeSignature)
    assert not abjad.get.has_indicator(staff[1])
    assert not abjad.get.has_indicator(staff[2])
    assert not abjad.get.has_indicator(staff[3])
    assert not abjad.get.has_indicator(staff)


def test_get_indicators_01():
    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.slur(voice[:])
    command_1 = abjad.LilyPondLiteral(r"\slurDotted", site="before")
    abjad.attach(command_1, voice[0])
    command_2 = abjad.LilyPondLiteral(r"\slurUp", site="before")
    abjad.attach(command_2, voice[0])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \slurDotted
            \slurUp
            c'8
            (
            d'8
            e'8
            f'8
            )
        }
        """
    ), abjad.lilypond(voice)

    indicators = abjad.get.indicators(voice[0], abjad.LilyPondLiteral)
    assert command_1 in indicators
    assert command_2 in indicators
    assert len(indicators) == 2


def test_get_indicators_02():
    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([voice])
    clef = abjad.Clef("treble")
    abjad.attach(clef, voice[0])
    dynamic = abjad.Dynamic("p")
    abjad.attach(dynamic, voice[0])

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                \clef "treble"
                c'8
                \p
                d'8
                e'8
                f'8
            }
        }
        """
    ), abjad.lilypond(staff)

    indicators = abjad.get.indicators(voice[0])
    assert len(indicators) == 2


def test_get_indicators_03():
    note = abjad.Note("c'4")
    stem_tremolo = abjad.StemTremolo(16)
    abjad.attach(stem_tremolo, note)
    stem_tremolos = abjad.get.indicators(note, abjad.StemTremolo)

    assert stem_tremolos[0] is stem_tremolo


def test_get_markup_01():
    chord = abjad.Chord([-11, 2, 5], (1, 4))
    up_markup = abjad.Markup(r"\markup UP")
    abjad.attach(up_markup, chord, direction=abjad.UP)
    down_markup = abjad.Markup(r"\markup DOWN")
    abjad.attach(down_markup, chord, direction=abjad.DOWN)
    found_markup = abjad.get.markup(chord, direction=abjad.DOWN)
    assert found_markup == [down_markup]


def test_get_markup_02():
    chord = abjad.Chord([-11, 2, 5], (1, 4))
    up_markup = abjad.Markup(r"\markup UP")
    abjad.attach(up_markup, chord, direction=abjad.UP)
    down_markup = abjad.Markup(r"\markup DOWN")
    abjad.attach(down_markup, chord, direction=abjad.DOWN)
    found_markup = abjad.get.markup(chord, direction=abjad.UP)
    assert found_markup == [up_markup]


def test_get_staff_01():
    """
    Staff changes work on the first note of a staff.
    """

    staff_group = abjad.StaffGroup(
        [abjad.Staff("c'8 d'8 e'8 f'8"), abjad.Staff("c'8 d'8 e'8 f'8")]
    )
    staff_group.lilypond_type = "PianoStaff"
    staff_group.simultaneous = True
    staff_group[0].name = "RH"
    staff_group[1].name = "LH"
    staff_change = abjad.StaffChange("LH")
    abjad.attach(staff_change, staff_group[0][0])

    assert abjad.lilypond(staff_group) == abjad.string.normalize(
        r"""
        \new PianoStaff
        <<
            \context Staff = "RH"
            {
                \change Staff = LH
                c'8
                d'8
                e'8
                f'8
            }
            \context Staff = "LH"
            {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        """
    )

    assert abjad.wf.wellformed(staff_group)
    assert abjad.get.effective_staff(staff_group[0][0]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][1]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][2]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][3]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][0]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][1]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][2]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][3]) is staff_group[1]


def test_get_staff_02():
    """
    Staff changes work on middle notes of a staff.
    """

    staff_group = abjad.StaffGroup(
        [abjad.Staff("c'8 d'8 e'8 f'8"), abjad.Staff("c'8 d'8 e'8 f'8")]
    )
    staff_group.lilypond_type = "PianoStaff"
    staff_group.simultaneous = True
    staff_group[0].name = "RH"
    staff_group[1].name = "LH"
    staff_change = abjad.StaffChange("LH")
    abjad.attach(staff_change, staff_group[0][0])
    staff_change = abjad.StaffChange("RH")
    abjad.attach(staff_change, staff_group[0][2])

    assert abjad.lilypond(staff_group) == abjad.string.normalize(
        r"""
        \new PianoStaff
        <<
            \context Staff = "RH"
            {
                \change Staff = LH
                c'8
                d'8
                \change Staff = RH
                e'8
                f'8
            }
            \context Staff = "LH"
            {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        """
    )

    assert abjad.wf.wellformed(staff_group)
    assert abjad.get.effective_staff(staff_group[0][0]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][1]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][2]) is staff_group[0]
    assert abjad.get.effective_staff(staff_group[0][3]) is staff_group[0]
    assert abjad.get.effective_staff(staff_group[1][0]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][1]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][2]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][3]) is staff_group[1]


def test_get_staff_03():
    """
    Staff changes work on the last note of a staff.
    """

    staff_group = abjad.StaffGroup(
        [abjad.Staff("c'8 d'8 e'8 f'8"), abjad.Staff("c'8 d'8 e'8 f'8")]
    )
    staff_group.lilypond_type = "PianoStaff"
    staff_group.simultaneous = True
    staff_group[0].name = "RH"
    staff_group[1].name = "LH"
    staff_change = abjad.StaffChange("LH")
    abjad.attach(staff_change, staff_group[0][-1])

    assert abjad.lilypond(staff_group) == abjad.string.normalize(
        r"""
        \new PianoStaff
        <<
            \context Staff = "RH"
            {
                c'8
                d'8
                e'8
                \change Staff = LH
                f'8
            }
            \context Staff = "LH"
            {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        """
    )

    assert abjad.wf.wellformed(staff_group)


def test_get_staff_04():
    """
    Redudant staff changes are allowed.
    """

    staff_group = abjad.StaffGroup(
        [abjad.Staff("c'8 d'8 e'8 f'8"), abjad.Staff("c'8 d'8 e'8 f'8")]
    )
    staff_group.lilypond_type = "PianoStaff"
    staff_group.simultaneous = True
    staff_group[0].name = "RH"
    staff_group[1].name = "LH"
    staff_change = abjad.StaffChange("LH")
    abjad.attach(staff_change, staff_group[0][0])
    staff_change = abjad.StaffChange("LH")
    abjad.attach(staff_change, staff_group[0][1])

    assert abjad.lilypond(staff_group) == abjad.string.normalize(
        r"""
        \new PianoStaff
        <<
            \context Staff = "RH"
            {
                \change Staff = LH
                c'8
                \change Staff = LH
                d'8
                e'8
                f'8
            }
            \context Staff = "LH"
            {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        """
    )

    assert abjad.wf.wellformed(staff_group)
    assert abjad.get.effective_staff(staff_group[0][0]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][1]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][2]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[0][3]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][0]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][1]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][2]) is staff_group[1]
    assert abjad.get.effective_staff(staff_group[1][3]) is staff_group[1]
