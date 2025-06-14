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


def test_makers_tuplet_from_proportion_and_pair_01():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((1, 2, 4), (6, 16))

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


def test_makers_tuplet_from_proportion_and_pair_02():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((1, 1, 2, 4), (6, 16))

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


def test_makers_tuplet_from_proportion_and_pair_03():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((-2, 3, 7), (7, 16))

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


def test_makers_tuplet_from_proportion_and_pair_04():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((7, 7, -4, -1), (1, 4))

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


def test_makers_tuplet_from_proportion_and_pair_05():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((1, 2, 2), (12, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/6
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_proportion_and_pair_06():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((2, 4, 4), (12, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/6
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_proportion_and_pair_07():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((4, 8, 8), (12, 16))

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


def test_makers_tuplet_from_proportion_and_pair_08():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((8, 16, 16), (12, 16))

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


def test_makers_tuplet_from_proportion_and_pair_09():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((2, 4, 4), (3, 16))

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


def test_makers_tuplet_from_proportion_and_pair_10():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((2, 4, 4), (6, 16))

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


def test_makers_tuplet_from_proportion_and_pair_11():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((2, 4, 4), (12, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/6
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_proportion_and_pair_12():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((2, 4, 4), (24, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/6
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_proportion_and_pair_13():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((1, 2, 2), (6, 2))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/6
        {
            c'2
            c'1
            c'1
        }
        """
    )


def test_makers_tuplet_from_proportion_and_pair_14():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((1, 2, 2), (6, 4))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/6
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_proportion_and_pair_15():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((1, 2, 2), (6, 8))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/6
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_proportion_and_pair_16():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((1, 2, 2), (6, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 5/6
        {
            c'16
            c'8
            c'8
        }
        """
    )


def test_makers_tuplet_from_proportion_and_pair_17():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((1, -1, -1), (3, 16))

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


def test_makers_tuplet_from_proportion_and_pair_18():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((1, 1, -1, -1), (4, 16))

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


def test_makers_tuplet_from_proportion_and_pair_19():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((1, 1, 1, -1, -1), (5, 16))

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


def test_makers_tuplet_from_proportion_and_pair_20():
    tuplet = abjad.makers.tuplet_from_proportion_and_pair((1, 1, 1, 1, -1, -1), (6, 16))

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
