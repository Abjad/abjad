# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_fuse_leaves_01():
    r'''Wokrs with list of leaves.
    '''

    fused = leaftools.fuse_leaves(notetools.make_repeated_notes(8, Duration(1, 4)))
    assert len(fused) == 1
    assert fused[0].written_duration == Duration(2)


def test_leaftools_fuse_leaves_02():
    r'''Works with Leaf component.
    '''

    fused = leaftools.fuse_leaves([Note("c'4")])
    assert len(fused) == 1
    assert fused[0].written_duration == Duration(1, 4)


def test_leaftools_fuse_leaves_03():
    r'''Works with containers.
    '''

    voice = Voice(Note("c'4") * 8)
    fused = leaftools.fuse_leaves(voice[:])
    assert len(fused) == 1
    assert fused[0].written_duration == 2
    assert voice[0] is fused[0]


def test_leaftools_fuse_leaves_04():
    r'''Fusion results in tied notes.
    '''

    voice = Voice([Note(0, (2, 16)), Note(9, (3, 16))])
    fused = leaftools.fuse_leaves(voice[:])
    assert len(fused) == 2
    assert fused[0].written_duration == Duration(1, 4)
    assert fused[1].written_duration == Duration(1, 16)
    tie_1 = inspect(fused[0]).get_spanner(spannertools.TieSpanner)
    tie_2 = inspect(fused[1]).get_spanner(spannertools.TieSpanner)
    assert tie_1 is tie_2
    assert voice[0] is fused[0]
    assert voice[1] is fused[1]
    assert voice[0].written_pitch.numbered_chromatic_pitch == voice[1].written_pitch.numbered_chromatic_pitch


def test_leaftools_fuse_leaves_05():
    r'''Fuse leaves with differing LilyPond multipliers.
    '''

    staff = Staff([skiptools.Skip((1, 1)), skiptools.Skip((1, 1))])
    staff[0].lilypond_duration_multiplier = Duration(1, 16)
    staff[1].lilypond_duration_multiplier = Duration(5, 16)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            s1 * 1/16
            s1 * 5/16
        }
        '''
        )

    assert inspect(staff).get_duration() == Duration(3, 8)

    leaftools.fuse_leaves(staff[:])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            s1 * 3/8
        }
        '''
        )

    assert inspect(staff).get_duration() == Duration(3, 8)
    assert inspect(staff).is_well_formed()
