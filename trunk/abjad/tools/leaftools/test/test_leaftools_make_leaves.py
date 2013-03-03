from abjad import *


def test_leaftools_make_leaves_01():
    '''Leaves constructor can create chords, notes and rests simultaneously.
    '''

    leaves = leaftools.make_leaves([1, (1,2,3), None], [(1, 4)])
    assert isinstance(leaves[0], Note)
    assert isinstance(leaves[1], Chord)
    assert isinstance(leaves[2], Rest)
    for l in leaves:
      assert l.written_duration == Duration(1, 4)


def test_leaftools_make_leaves_02():
    '''Leaves constructor can create prolated chords, notes and rests
    simultaneously. Contiguous leaves with the same prolation are
    put together inside a tuplet.
    '''

    leaves = leaftools.make_leaves([1, (1, 2, 3), None], [(2, 9), (1, 18), (1,5)])
    assert isinstance(leaves[0], Tuplet)
    assert isinstance(leaves[1], Tuplet)
    tuplet1 = leaves[0]
    assert len(tuplet1) == 2
    assert tuplet1.multiplier == Duration(8, 9)
    assert isinstance(tuplet1[0], Note)
    assert isinstance(tuplet1[1], Chord)
    tuplet2 = leaves[1]
    assert len(tuplet2) == 1
    assert tuplet2.multiplier == Duration(4, 5)
    assert isinstance(tuplet2[0], Rest)

    assert tuplet1[0].written_duration == Duration(2, 8)
    assert tuplet1[1].written_duration == Duration(1, 16)
    assert tuplet2[0].written_duration == Duration(1, 4)


def test_leaftools_make_leaves_03():
    '''Leaves constructor can create prolated and unprolated chords,
    notes and rests simultaneously.
    '''

    leaves = leaftools.make_leaves([1, (1,2,3), None], [(2, 9), (1,8), (1,5)])
    assert isinstance(leaves[0], Tuplet)
    assert isinstance(leaves[1], Chord)
    assert isinstance(leaves[2], Tuplet)
    tuplet1 = leaves[0]
    assert len(tuplet1) == 1
    assert tuplet1.multiplier == Duration(8, 9)
    assert isinstance(tuplet1[0], Note)
    tuplet2 = leaves[2]
    assert len(tuplet2) == 1
    assert tuplet2.multiplier == Duration(4, 5)
    assert isinstance(tuplet2[0], Rest)


def test_leaftools_make_leaves_04():
    '''Leaves constructor can take an optional tie_rests=False keyword argument.
    '''

    leaves = leaftools.make_leaves([None], [(5, 32), (5, 32)], tie_rests=True)
    assert len(leaves) == 4
    for l in leaves:
      assert isinstance(l, Rest)
    assert spannertools.get_the_only_spanner_attached_to_component(
      leaves[0], tietools.TieSpanner) is \
      spannertools.get_the_only_spanner_attached_to_component(
      leaves[1], tietools.TieSpanner)
    assert spannertools.get_the_only_spanner_attached_to_component(
      leaves[2], tietools.TieSpanner) is \
      spannertools.get_the_only_spanner_attached_to_component(
      leaves[3], tietools.TieSpanner)


def test_leaftools_make_leaves_05():
    '''Do not tie rests unless specified.
    '''

    leaves = leaftools.make_leaves([None], [(5, 32), (5, 32)])
    assert len(leaves) == 4
    for l in leaves:
      assert isinstance(l, Rest)
      assert not tietools.is_component_with_tie_spanner_attached(l)


def test_leaftools_make_leaves_06():
    '''Works with quarter-tone pitch numbers.
    '''

    leaves = leaftools.make_leaves([12, 12.5, 13, 13.5], [(1, 4)])
    assert [leaf.written_pitch.numbered_chromatic_pitch._chromatic_pitch_number for leaf in leaves] == \
        [12, 12.5, 13, 13.5]


def test_leaftools_make_leaves_07():
    '''Works with pitch instances.
    '''

    leaves = leaftools.make_leaves([pitchtools.NamedChromaticPitch(0)], [(1, 8), (1, 8), (1, 4)])
    assert [leaf.written_pitch.numbered_chromatic_pitch._chromatic_pitch_number for leaf in leaves] == [0, 0, 0]


def test_leaftools_make_leaves_08():
    '''Chords work with pitch-class / octave strings.
    '''

    leaves = leaftools.make_leaves([('C#5', 'Db5')], [Duration(1, 4), Duration(1, 8)])
    staff = Staff(leaves)

    r'''
    \new Staff {
        <cs'' df''>4
        <cs'' df''>8
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t<cs'' df''>4\n\t<cs'' df''>8\n}"


def test_leaftools_make_leaves_09():
    '''Notes work with pitch-class / octave strings.
    '''

    leaves = leaftools.make_leaves(['C#5', 'Db5'], [Duration(1, 4)])
    staff = Staff(leaves)

    r'''
    \new Staff {
        cs''4
        df''4
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tcs''4\n\tdf''4\n}"


def test_leaftools_make_leaves_10():
    '''Works with space-delimited string of chromatic pitch names.
    '''

    leaves = leaftools.make_leaves("C#5 Db5 c'' fs''", [Duration(1, 4)])
    staff = Staff(leaves)

    r'''
    \new Staff {
        cs''4
        df''4
        c''4
        fs''4
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tcs''4\n\tdf''4\n\tc''4\n\tfs''4\n}"
