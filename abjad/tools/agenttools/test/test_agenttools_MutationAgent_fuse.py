# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_agenttools_MutationAgent_fuse_01():
    r'''Works with list of leaves.
    '''

    notes = 8 * Note("c'4")
    fused = mutate(notes).fuse()

    assert len(fused) == 1
    assert fused[0].written_duration == Duration(2)


def test_agenttools_MutationAgent_fuse_02():
    r'''Works with Leaf component.
    '''

    fused = mutate(Note("c'4")).fuse()
    assert len(fused) == 1
    assert fused[0].written_duration == Duration(1, 4)


def test_agenttools_MutationAgent_fuse_03():
    r'''Works with containers.
    '''

    voice = Voice(8 * Note("c'4"))
    fused = mutate(voice[:]).fuse()
    assert len(fused) == 1
    assert fused[0].written_duration == 2
    assert voice[0] is fused[0]


def test_agenttools_MutationAgent_fuse_04():
    r'''Fusion results in tied notes.
    '''

    voice = Voice([Note(0, (2, 16)), Note(9, (3, 16))])
    fused = mutate(voice[:]).fuse()

    assert len(fused) == 2
    assert fused[0].written_duration == Duration(1, 4)
    assert fused[1].written_duration == Duration(1, 16)

    tie_1 = inspect_(fused[0]).get_spanner(Tie)
    tie_2 = inspect_(fused[1]).get_spanner(Tie)

    assert tie_1 is tie_2
    assert voice[0] is fused[0]
    assert voice[1] is fused[1]
    assert voice[0].written_pitch == voice[1].written_pitch


def test_agenttools_MutationAgent_fuse_05():
    r'''Fuses leaves with differing LilyPond multipliers.
    '''

    staff = Staff([scoretools.Skip((1, 1)), scoretools.Skip((1, 1))])
    attach(Multiplier(1, 16), staff[0])
    attach(Multiplier(5, 16), staff[1])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            s1 * 1/16
            s1 * 5/16
        }
        '''
        )

    assert inspect_(staff).get_duration() == Duration(3, 8)

    mutate(staff[:]).fuse()

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            s1 * 3/8
        }
        '''
        )

    assert inspect_(staff).get_duration() == Duration(3, 8)
    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_fuse_06():
    r'''Fuses two unincorporated fixed-duration tuplets with same multiplier.
    '''

    tuplet_1 = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    beam = Beam()
    attach(beam, tuplet_1[:])
    tuplet_2 = scoretools.FixedDurationTuplet((2, 16), "c'16 d'16 e'16")
    slur = Slur()
    attach(slur, tuplet_2[:])

    assert format(tuplet_1) == stringtools.normalize(
        r'''
        \times 2/3 {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    assert format(tuplet_2) == stringtools.normalize(
        r'''
        \times 2/3 {
            c'16 (
            d'16
            e'16 )
        }
        '''
        )

    tuplets = select([tuplet_1, tuplet_2])
    new = mutate(tuplets).fuse()

    assert format(new) == stringtools.normalize(
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
    assert inspect_(new).is_well_formed()


def test_agenttools_MutationAgent_fuse_07():
    r'''Fuses fixed-duration tuplets with same multiplier in score.
    '''

    tuplet_1 = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    beam = Beam()
    attach(beam, tuplet_1[:])
    tuplet_2 = scoretools.FixedDurationTuplet((2, 16), "c'16 d'16 e'16")
    slur = Slur()
    attach(slur, tuplet_2[:])
    voice = Voice([tuplet_1, tuplet_2])

    assert format(voice) == stringtools.normalize(
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

    assert format(voice) == stringtools.normalize(
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

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_fuse_08():
    r'''Fuses fixed-multiplier tuplets with same multiplier in score.
    '''

    tuplet_1 = Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
    beam = Beam()
    attach(beam, tuplet_1[:])
    tuplet_2 = Tuplet(Multiplier(2, 3), "c'8 d'8 e'8 f'8 g'8")
    slur = Slur()
    attach(slur, tuplet_2[:])
    voice = Voice([tuplet_1, tuplet_2])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
            }
            \tweak edge-height #'(0.7 . 0)
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

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \tweak edge-height #'(0.7 . 0)
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

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_fuse_09():
    r'''Tuplets must carry same multiplier.
    '''

    tuplet_1 = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    tuplet_2 = scoretools.FixedDurationTuplet(Duration(2, 8), [])
    tuplet_2.extend("c'8 d'8 e'8 f'8 g'8")
    tuplets = select([tuplet_1, tuplet_2])

    assert pytest.raises(Exception, 'mutate(tuplets).fuse()')


def test_agenttools_MutationAgent_fuse_10():
    r'''Tuplets must be same type.
    '''

    tuplet_1 = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    tuplet_2 = Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
    tuplets = select([tuplet_1, tuplet_2])

    assert pytest.raises(Exception, 'mutate(tuplets).fuse()')


def test_agenttools_MutationAgent_fuse_11():
    r'''Dominant spanners on contents are preserved.
    '''

    tuplet_1 = scoretools.FixedDurationTuplet(Duration(1, 12), "c'8")
    tuplet_2 = scoretools.FixedDurationTuplet(Duration(1, 6), "c'4")
    voice = Voice([tuplet_1, tuplet_2, Note("c'4")])
    leaves = select(voice).by_leaf()
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8 (
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'4
            }
            c'4 )
        }
        '''
        )

    tuplets = voice[:2]
    mutate(tuplets).fuse()

    assert format(voice) == stringtools.normalize(
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

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_fuse_12():
    r'''Fuses unicorporated measures carrying
    time signatures with power-of-two denominators.
    '''

    measure_1 = Measure((1, 8), "c'16 d'16")
    beam = Beam()
    attach(beam, measure_1[:])
    measure_2 = Measure((2, 16), "c'16 d'16")
    slur = Slur()
    attach(slur, measure_2[:])
    staff = Staff([measure_1, measure_2])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 1/8
                c'16 [
                d'16 ]
            }
            {
                \time 2/16
                c'16 (
                d'16 )
            }
        }
        '''
        )

    new = mutate(staff[:]).fuse()

    assert new is not measure_1 and new is not measure_2
    assert len(measure_1) == 0
    assert len(measure_2) == 0

    assert format(new) == stringtools.normalize(
        r'''
        {
            \time 2/8
            c'16 [
            d'16 ]
            c'16 (
            d'16 )
        }
        '''
        )

    assert inspect_(new).is_well_formed()


def test_agenttools_MutationAgent_fuse_13():
    r'''Fuses measures carrying time signatures with differing
    power-of-two denominators. Helpers selects minimum of two denominators.
    Beams are OK because they attach to leaves rather than containers.
    '''

    voice = Voice("abj: | 1/8 c'16 d'16 || 2/16 e'16 f'16 |")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 1/8
                c'16 [
                d'16
            }
            {
                \time 2/16
                e'16
                f'16 ]
            }
        }
        '''
        )

    mutate(voice[:]).fuse()

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                c'16 [
                d'16
                e'16
                f'16 ]
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_fuse_14():
    r'''Fuses measures with differing power-of-two denominators.
    Helpers selects minimum of two denominators.
    Beam attaches to container rather than leaves.
    '''

    voice = Voice("abj: | 1/8 c'16 d'16 || 2/16 e'16 f'16 |")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves[:2])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 1/8
                c'16 [
                d'16 ]
            }
            {
                \time 2/16
                e'16
                f'16
            }
        }
        '''
        )

    mutate(voice[:]).fuse()

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                c'16 [
                d'16 ]
                e'16
                f'16
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_fuse_15():
    r'''Fuses measures with power-of-two-denominators together with measures
    without power-of-two denominators.
    Helpers selects least common multiple of denominators.
    Beams are OK because they attach to leaves rather than containers.
    '''

    measure_1 = Measure((1, 8), "c'8")
    measure_1.implicit_scaling = True
    measure_2 = Measure((1, 12), "d'8")
    measure_2.implicit_scaling = True
    voice = Voice([measure_1, measure_2])
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 1/8
                c'8 [
            }
            {
                \time 1/12
                \scaleDurations #'(2 . 3) {
                    d'8 ]
                }
            }
        }
        '''
        )

    mutate(voice[:]).fuse()

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 5/24
                \scaleDurations #'(2 . 3) {
                    c'8. [
                    d'8 ]
                }
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_fuse_16():
    r'''Fusing empty selection returns none.
    '''

    staff = Staff()
    result = mutate(staff[:]).fuse()
    assert result == selectiontools.Selection()


def test_agenttools_MutationAgent_fuse_17():
    r'''Fusing selection of only one measure returns measure unaltered.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")
    staff = Staff([measure])
    new = mutate(staff[:]).fuse()

    assert new is measure


def test_agenttools_MutationAgent_fuse_18():
    r'''Fuses three measures.
    '''

    voice = Voice("abj: | 1/8 c'16 d'16 || 1/8 e'16 f'16 || 1/8 g'16 a'16 |")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 1/8
                c'16 [
                d'16
            }
            {
                e'16
                f'16
            }
            {
                g'16
                a'16 ]
            }
        }
        '''
        )

    mutate(voice[:]).fuse()

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 3/8
                c'16 [
                d'16
                e'16
                f'16
                g'16
                a'16 ]
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_fuse_19():
    r'''Fusing measures with power-of-two denominators
    to measures without power-of-two denominators.
    With change in number of note heads because of non-power-of-two multiplier.
    '''

    measure_1 = Measure((9, 80), [])
    measure_1.implicit_scaling = True
    measure_2 = Measure((2, 16), [])
    measure_2.implicit_scaling = True
    staff = Staff([measure_1, measure_2])
    scoretools.fill_measures_in_expr_with_time_signature_denominator_notes(
        staff)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 9/80
                \scaleDurations #'(4 . 5) {
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                }
            }
            {
                \time 2/16
                c'16
                c'16
            }
        }
        '''
        )

    new = mutate(staff[:]).fuse()

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 19/80
                \scaleDurations #'(4 . 5) {
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'16 ~
                    c'64
                    c'16 ~
                    c'64
                }
            }
        }
        '''
        )

    assert inspect_(staff).is_well_formed()
