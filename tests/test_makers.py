import pytest

import abjad


def test_makers__group_by_prolation_01():
    with pytest.raises(Exception):
        abjad.makers._group_by_prolation([])


def test_makers__group_by_prolation_02():
    pairs = [(1, 4)]
    durations = [abjad.Duration(_) for _ in pairs]
    duration_lists = abjad.makers._group_by_prolation(durations)
    assert duration_lists == [[abjad.Duration(1, 4)]]


def test_makers__group_by_prolation_03():
    pairs = [(1, 4), (1, 4), (1, 8)]
    durations = [abjad.Duration(_) for _ in pairs]
    duration_lists = abjad.makers._group_by_prolation(durations)
    assert duration_lists == [
        [
            abjad.Duration(1, 4),
            abjad.Duration(1, 4),
            abjad.Duration(1, 8),
        ]
    ]


def test_makers__group_by_prolation_04():
    pairs = [(1, 4), (1, 3), (1, 8)]
    durations = [abjad.Duration(_) for _ in pairs]
    duration_lists = abjad.makers._group_by_prolation(durations)
    assert duration_lists == [
        [abjad.Duration(1, 4)],
        [abjad.Duration(1, 3)],
        [abjad.Duration(1, 8)],
    ]


def test_makers__group_by_prolation_05():
    pairs = [(1, 4), (1, 2), (1, 3)]
    durations = [abjad.Duration(_) for _ in pairs]
    duration_lists = abjad.makers._group_by_prolation(durations)
    assert duration_lists == [
        [abjad.Duration(1, 4), abjad.Duration(1, 2)],
        [abjad.Duration(1, 3)],
    ]


def test_makers__group_by_prolation_06():
    pairs = [(1, 4), (1, 2), (1, 3), (1, 6), (1, 5)]
    durations = [abjad.Duration(_) for _ in pairs]
    duration_lists = abjad.makers._group_by_prolation(durations)
    assert duration_lists == [
        [abjad.Duration(1, 4), abjad.Duration(1, 2)],
        [abjad.Duration(1, 3), abjad.Duration(1, 6)],
        [abjad.Duration(1, 5)],
    ]


def test_makers__group_by_prolation_07():
    pairs = [(1, 24), (2, 24), (3, 24), (4, 24), (5, 24), (6, 24)]
    durations = [abjad.Duration(_) for _ in pairs]
    duration_lists = abjad.makers._group_by_prolation(durations)
    assert duration_lists == [
        [abjad.Duration(1, 24), abjad.Duration(2, 24)],
        [abjad.Duration(3, 24)],
        [abjad.Duration(4, 24), abjad.Duration(5, 24)],
        [abjad.Duration(6, 24)],
    ]


def test_makers_make_notes_01():
    """
    Tag output like this.
    """

    pitches = abjad.makers.make_pitches([0])
    durations = abjad.makers.make_durations([(1, 16), (1, 8), (1, 8)])
    tag = abjad.Tag("note_maker")
    notes = abjad.makers.make_notes(pitches, durations, tag=tag)
    staff = abjad.Staff(notes)
    string = abjad.lilypond(staff, tags=True)

    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
              %! note_maker
            c'16
              %! note_maker
            c'8
              %! note_maker
            c'8
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_01():
    duration = abjad.Duration(6, 16)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (1, 2, 4))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 7/6
        {
            c'16
            c'8
            c'4
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_02():
    duration = abjad.Duration(6, 16)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (1, 1, 2, 4))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 4/3
        {
            c'16
            c'16
            c'8
            c'4
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_03():
    duration = abjad.Duration(7, 16)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (-2, 3, 7))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 12/7
        {
            r8
            c'8.
            c'4..
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_04():
    duration = abjad.Duration(1, 4)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (7, 7, -4, -1))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 19/16
        {
            c'16..
            c'16..
            r16
            r64
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_05():
    duration = abjad.Duration(12, 16)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (1, 2, 2))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/3
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_06():
    duration = abjad.Duration(12, 16)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (2, 4, 4))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/3
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_07():
    duration = abjad.Duration(12, 16)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (4, 8, 8))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/3
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_08():
    duration = abjad.Duration(12, 16)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (8, 16, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/3
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_09():
    duration = abjad.Duration(3, 16)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (2, 4, 4))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/3
        {
            c'16
            c'8
            c'8
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_10():
    duration = abjad.Duration(6, 16)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (2, 4, 4))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/3
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_11():
    duration = abjad.Duration(12, 16)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (2, 4, 4))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/3
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_12():
    duration = abjad.Duration(24, 16)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (2, 4, 4))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/3
        {
            c'2
            c'1
            c'1
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_13():
    duration = abjad.Duration(6, 2)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (1, 2, 2))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/3
        {
            c'1
            c'\breve
            c'\breve
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_14():
    duration = abjad.Duration(6, 4)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (1, 2, 2))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/3
        {
            c'2
            c'1
            c'1
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_15():
    duration = abjad.Duration(6, 8)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (1, 2, 2))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/3
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_16():
    duration = abjad.Duration(6, 16)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (1, 2, 2))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/3
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_17():
    duration = abjad.Duration(3, 16)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (1, -1, -1))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 1/1
        {
            c'16
            r16
            r16
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_18():
    duration = abjad.Duration(4, 16)
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(duration, (1, 1, -1, -1))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 1/1
        {
            c'16
            c'16
            r16
            r16
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_19():
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(
        abjad.Duration(5, 16),
        (1, 1, 1, -1, -1),
    )

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 1/1
        {
            c'16
            c'16
            c'16
            r16
            r16
        }
        """
    )


def test_makers_tuplet_from_duration_and_proportion_20():
    tuplet = abjad.makers.tuplet_from_duration_and_proportion(
        abjad.Duration(6, 16),
        (1, 1, 1, 1, -1, -1),
    )

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 1/1
        {
            c'16
            c'16
            c'16
            c'16
            r16
            r16
        }
        """
    )
