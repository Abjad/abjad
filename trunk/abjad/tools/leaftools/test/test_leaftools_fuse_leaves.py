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
    #assert fused[0].tie.spanner is fused[1].tie.spanner
    assert spannertools.get_the_only_spanner_attached_to_component(
      fused[0], spannertools.TieSpanner) is \
      spannertools.get_the_only_spanner_attached_to_component(
      fused[1], spannertools.TieSpanner)
    assert voice[0] is fused[0]
    assert voice[1] is fused[1]
    assert voice[0].written_pitch.numbered_chromatic_pitch == voice[1].written_pitch.numbered_chromatic_pitch


def test_leaftools_fuse_leaves_05():
    r'''Fuse leaves with differing LilyPond multipliers.
    '''

    staff = Staff([skiptools.Skip((1, 1)), skiptools.Skip((1, 1))])
    staff[0].lilypond_duration_multiplier = Duration(1, 16)
    staff[1].lilypond_duration_multiplier = Duration(5, 16)

    r'''
    \new Staff {
      s1 * 1/16
      s1 * 5/16
    }
    '''

    assert inspect(staff).get_duration() == Duration(3, 8)

    result = leaftools.fuse_leaves(staff[:])

    r'''
    \new Staff {
      s1 * 3/8
    }
    '''

    assert select(staff).is_well_formed()
    assert len(result) == 1
    assert inspect(staff).get_duration() == Duration(3, 8)
