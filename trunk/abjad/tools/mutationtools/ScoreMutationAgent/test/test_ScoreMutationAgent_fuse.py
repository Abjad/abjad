# -*- encoding: utf-8 -*-
import py
from abjad import *


def test_ScoreMutationAgent_fuse_01():
    r'''Works with list of leaves.
    '''

    notes = notetools.make_repeated_notes(8, Duration(1, 4))
    fused = mutate(notes).fuse()

    assert len(fused) == 1
    assert fused[0].written_duration == Duration(2)


def test_ScoreMutationAgent_fuse_02():
    r'''Works with Leaf component.
    '''

    fused = mutate(Note("c'4")).fuse()
    assert len(fused) == 1
    assert fused[0].written_duration == Duration(1, 4)


def test_ScoreMutationAgent_fuse_03():
    r'''Works with containers.
    '''

    voice = Voice(Note("c'4") * 8)
    fused = mutate(voice[:]).fuse()
    assert len(fused) == 1
    assert fused[0].written_duration == 2
    assert voice[0] is fused[0]


def test_ScoreMutationAgent_fuse_04():
    r'''Fusion results in tied notes.
    '''

    voice = Voice([Note(0, (2, 16)), Note(9, (3, 16))])
    fused = mutate(voice[:]).fuse()
    assert len(fused) == 2
    assert fused[0].written_duration == Duration(1, 4)
    assert fused[1].written_duration == Duration(1, 16)
    tie_1 = inspect(fused[0]).get_spanner(spannertools.TieSpanner)
    tie_2 = inspect(fused[1]).get_spanner(spannertools.TieSpanner)
    assert tie_1 is tie_2
    assert voice[0] is fused[0]
    assert voice[1] is fused[1]
    assert voice[0].written_pitch.numbered_chromatic_pitch == \
        voice[1].written_pitch.numbered_chromatic_pitch


def test_ScoreMutationAgent_fuse_05():
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

    mutate(staff[:]).fuse()

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


def test_ScoreMutationAgent_fuse_06():
    r'''Fuse two unincorporated fixed-duration tuplets with same multiplier.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    spannertools.BeamSpanner(tuplet_1[:])
    tuplet_2 = tuplettools.FixedDurationTuplet(Duration(2, 16), "c'16 d'16 e'16")
    spannertools.SlurSpanner(tuplet_2[:])

    assert testtools.compare(
        tuplet_1,
        r'''
        \times 2/3 {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    assert testtools.compare(
        tuplet_2,
        r'''
        \times 2/3 {
            c'16 (
            d'16
            e'16 )
        }
        '''
        )

    tuplets = select([tuplet_1, tuplet_2], contiguous=True)
    new = mutate(tuplets).fuse()

    assert testtools.compare(
        new,
        r'''
        \times 2/3 {
            c'8 [
            d'8
            e'8 ]
            c'16 (
            d'16
            e'16 )
        }
        '''
        )

    assert len(tuplet_1) == 0
    assert len(tuplet_2) == 0
    assert new is not tuplet_1 and new is not tuplet_2
    assert inspect(new).is_well_formed()


def test_ScoreMutationAgent_fuse_07():
    r'''Fuse fixed-duration tuplets with same multiplier in score.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    spannertools.BeamSpanner(tuplet_1[:])
    tuplet_2 = tuplettools.FixedDurationTuplet(Duration(2, 16), "c'16 d'16 e'16")
    spannertools.SlurSpanner(tuplet_2[:])
    voice = Voice([tuplet_1, tuplet_2])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
            }
            \times 2/3 {
                c'16 (
                d'16
                e'16 )
            }
        }
        '''
        )

    tuplets = voice[:]
    mutate(tuplets).fuse()

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
                c'16 (
                d'16
                e'16 )
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_ScoreMutationAgent_fuse_08():
    r'''Fuse fixed-multiplier tuplets with same multiplier in score.
    '''

    tuplet_1 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
    spannertools.BeamSpanner(tuplet_1[:])
    tuplet_2 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8 f'8 g'8")
    spannertools.SlurSpanner(tuplet_2[:])
    voice = Voice([tuplet_1, tuplet_2])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
            }
            \times 2/3 {
                c'8 (
                d'8
                e'8
                f'8
                g'8 )
            }
        }
        '''
        )

    tuplets = voice[:]
    mutate(tuplets).fuse()

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
                c'8 (
                d'8
                e'8
                f'8
                g'8 )
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_ScoreMutationAgent_fuse_09():
    r'''Tuplets must carry same multiplier.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    tuplet_2 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8 f'8 g'8")
    tuplets = select([tuplet_1, tuplet_2], contiguous=True)

    assert py.test.raises(Exception, 'mutate(tuplets).fuse()')


def test_ScoreMutationAgent_fuse_10():
    r'''Tuplets must be same type.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    tuplet_2 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
    tuplets = select([tuplet_1, tuplet_2], contiguous=True)

    assert py.test.raises(Exception, 'mutate(tuplets).fuse()')


def test_ScoreMutationAgent_fuse_11():
    r'''Dominant spanners on contents are preserved.
    '''

    voice = Voice([
        tuplettools.FixedDurationTuplet(Duration(1, 12), [Note(0, (1, 8))]),
        tuplettools.FixedDurationTuplet(Duration(1, 6), [Note("c'4")]),
        Note("c'4")])
    spannertools.SlurSpanner(voice.select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 (
            }
            \times 2/3 {
                c'4
            }
            c'4 )
        }
        '''
        )

    tuplets = voice[:2]
    mutate(tuplets).fuse()

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 (
                c'4
            }
            c'4 )
        }
        '''
        )

    assert inspect(voice).is_well_formed()
