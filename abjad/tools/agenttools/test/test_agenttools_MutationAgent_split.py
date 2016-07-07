# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_agenttools_MutationAgent_split_01():
    r'''Cyclically splits note in score. Doesn't fracture spanners.
    '''

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    notes = staff[0][1:2]
    result = mutate(notes).split(
        [Duration(3, 64)],
        cyclic=True,
        fracture_spanners=False,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'32. ~
                d'32. ~
                d'32 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_02():
    r'''Cyclically splits consecutive notes in score.
    Doesn't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    result = mutate(leaves).split(
        [Duration(3, 32)],
        cyclic=True,
        fracture_spanners=False,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'16. ~ [ (
                c'32
                d'16 ~
                d'16 ]
            }
            {
                e'32 ~ [
                e'16.
                f'16. ~
                f'32 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_03():
    r'''Cyclically splits measure in score. Doesn't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True,
        fracture_spanners=False,
        tie_split_notes=False,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ (
            }
            {
                c'32
                d'16
            }
            {
                \time 2/32
                d'16 ]
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_04():
    r'''Cyclically splits consecutive measures in score.
    Doesn't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    measures = staff[:]
    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True,
        fracture_spanners=False,
        tie_split_notes=False,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ (
            }
            {
                c'32
                d'16
            }
            {
                \time 2/32
                d'16 ]
            }
            {
                \time 1/32
                e'32 [
            }
            {
                \time 3/32
                e'16.
            }
            {
                f'16.
            }
            {
                \time 1/32
                f'32 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_05():
    r'''Cyclically splits orphan measures. Doesn't fracture spanners.
    '''

    measures = [Measure((2, 8), "c'8 d'8"), Measure((2, 8), "e'8 f'8")]
    leaves = select(measures).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])

    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True,
        fracture_spanners=False,
        tie_split_notes=False,
        )

    music = sequencetools.flatten_sequence(result)
    staff = Staff(music)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [
            }
            {
                c'32
                d'16
            }
            {
                \time 2/32
                d'16 ]
            }
            {
                \time 1/32
                e'32 [
            }
            {
                \time 3/32
                e'16.
            }
            {
                f'16.
            }
            {
                \time 1/32
                f'32 ]
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_06():
    r'''Cyclically splits note in score. Doesn't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    notes = staff[0][1:]
    result = mutate(notes).split(
        [Duration(1, 32)],
        cyclic=True,
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'32 ~
                d'32 ~
                d'32 ~
                d'32 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 4


def test_agenttools_MutationAgent_split_07():
    r'''Cyclically splits consecutive notes in score.
    Doesn't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    result = mutate(leaves).split(
        [Duration(1, 16)],
        cyclic=True,
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'16 ~ [ (
                c'16
                d'16 ~
                d'16 ]
            }
            {
                e'16 ~ [
                e'16
                f'16 ~
                f'16 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 8


def test_agenttools_MutationAgent_split_08():
    r'''Cyclically splits measure in score. Doesn't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(1, 16)],
        cyclic=True,
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 1/16
                c'16 ~ [ (
            }
            {
                c'16
            }
            {
                d'16 ~
            }
            {
                d'16 ]
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 4


def test_agenttools_MutationAgent_split_09():
    r'''Cyclically splits consecutive measures in score.
    Doesn't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    measures = staff[:]
    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True,
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. ~ [ (
            }
            {
                c'32
                d'16 ~
            }
            {
                \time 2/32
                d'16 ]
            }
            {
                \time 1/32
                e'32 ~ [
            }
            {
                \time 3/32
                e'16.
            }
            {
                f'16. ~
            }
            {
                \time 1/32
                f'32 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_10():
    r'''Cyclically splits note in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    notes = staff[0][1:2]
    result = mutate(notes).split(
        [Duration(3, 64)],
        cyclic=True,
        fracture_spanners=True,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'32. ~ ] )
                d'32. ~ [ ]
                d'32 [ ] (
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_11():
    r'''Cyclically splits consecutive notes in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    result = mutate(leaves).split(
        [Duration(3, 32)],
        cyclic=True,
        fracture_spanners=True,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'16. ~ [ ]
                c'32 [ (
                d'16 ~ ] )
                d'16 [ ] (
            }
            {
                e'32 ~ ) [ ]
                e'16. [ (
                f'16. ~ ] )
                f'32 [ ]
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_12():
    r'''Cyclically splits measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True,
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ ]
            }
            {
                c'32 [ (
                d'16 ] )
            }
            {
                \time 2/32
                d'16 [ ] (
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_13():
    r'''Cyclically splits consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    measures = staff[:]
    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True,
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ ]
            }
            {
                c'32 [ (
                d'16 ] )
            }
            {
                \time 2/32
                d'16 [ ] (
            }
            {
                \time 1/32
                e'32 ) [ ]
            }
            {
                \time 3/32
                e'16. [ ]
            }
            {
                f'16. [ ]
            }
            {
                \time 1/32
                f'32 [ ]
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_14():
    r'''Cyclically splits orphan notes.
    '''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]

    result = mutate(notes).split(
        [Duration(3, 32)],
        cyclic=True,
        fracture_spanners=True,
        )

    music = sequencetools.flatten_sequence(result)
    staff = Staff(music)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'16. ~
            c'32
            d'16 ~
            d'16
            e'32 ~
            e'16.
            f'16. ~
            f'32
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_15():
    r'''Cyclically splits orphan measures. Fracture spanners.
    '''

    measures = [Measure((2, 8), "c'8 d'8"), Measure((2, 8), "e'8 f'8")]
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, measures[0][:])
    attach(beam_2, measures[1][:])

    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True,
        fracture_spanners=True,
        tie_split_notes=False,
        )

    music = sequencetools.flatten_sequence(result)
    staff = Staff(music)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ ]
            }
            {
                c'32 [
                d'16 ]
            }
            {
                \time 2/32
                d'16 [ ]
            }
            {
                \time 1/32
                e'32 [ ]
            }
            {
                \time 3/32
                e'16. [ ]
            }
            {
                f'16. [ ]
            }
            {
                \time 1/32
                f'32 [ ]
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_16():
    r'''Cyclically splits note in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    notes = staff[0][1:]
    result = mutate(notes).split(
        [Duration(1, 32)],
        cyclic=True,
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'32 ~ ] )
                d'32 ~ [ ]
                d'32 ~ [ ]
                d'32 [ ] (
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 4


def test_agenttools_MutationAgent_split_17():
    r'''Cyclically splits consecutive notes in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    result = mutate(leaves).split(
        [Duration(1, 16)],
        cyclic=True,
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'16 ~ [ ]
                c'16 [ (
                d'16 ~ ] )
                d'16 [ ] (
            }
            {
                e'16 ~ ) [ ]
                e'16 [ (
                f'16 ~ ] )
                f'16 [ ]
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 8


def test_agenttools_MutationAgent_split_18():
    r'''Cyclically splits measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(1, 16)],
        cyclic=True,
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 1/16
                c'16 ~ [ ]
            }
            {
                c'16 [ ]
            }
            {
                d'16 ~ [ ]
            }
            {
                d'16 [ ] (
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 4


def test_agenttools_MutationAgent_split_19():
    r'''Cyclically splits consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    measures = staff[:]
    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True,
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. ~ [ ]
            }
            {
                c'32 [ (
                d'16 ~ ] )
            }
            {
                \time 2/32
                d'16 [ ] (
            }
            {
                \time 1/32
                e'32 ~ ) [ ]
            }
            {
                \time 3/32
                e'16. [ ]
            }
            {
                f'16. ~ [ ]
            }
            {
                \time 1/32
                f'32 [ ]
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_20():
    r'''Force splits measure in score. Do not fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(1, 32), Duration(3, 32), Duration(5, 32)],
        cyclic=False,
        fracture_spanners=False,
        tie_split_notes=False,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 1/32
                c'32 [ (
            }
            {
                \time 3/32
                c'16.
            }
            {
                \time 4/32
                d'8 ]
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_21():
    r'''Force splits consecutive measures in score. Do not fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    measures = staff[:]
    result = mutate(measures).split(
        [Duration(1, 32), Duration(3, 32), Duration(5, 32)],
        cyclic=False,
        fracture_spanners=False,
        tie_split_notes=False,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 1/32
                c'32 [ (
            }
            {
                \time 3/32
                c'16.
            }
            {
                \time 4/32
                d'8 ]
            }
            {
                \time 1/32
                e'32 [
            }
            {
                \time 7/32
                e'16.
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 4


def test_agenttools_MutationAgent_split_22():
    r'''Force splits measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(1, 32), Duration(3, 32), Duration(5, 32)],
        cyclic=False,
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 1/32
                c'32 [ ]
            }
            {
                \time 3/32
                c'16. [ ]
            }
            {
                \time 4/32
                d'8 [ ] (
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_23():
    r'''Force splits consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = select(staff).by_leaf()
    beam_1 = Beam()
    beam_2 = Beam()
    attach(beam_1, leaves[:2])
    attach(beam_2, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    measures = staff[:]
    result = mutate(measures).split(
        [Duration(1, 32), Duration(3, 32), Duration(5, 32)],
        cyclic=False,
        fracture_spanners=True,
        tie_split_notes=False)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 4
    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 1/32
                c'32 [ ]
            }
            {
                \time 3/32
                c'16. [ ]
            }
            {
                \time 4/32
                d'8 [ ] (
            }
            {
                \time 1/32
                e'32 ) [ ]
            }
            {
                \time 7/32
                e'16. [ (
                f'8 ] )
            }
        }
        '''
        ), format(staff)


def test_agenttools_MutationAgent_split_24():
    r'''Force splits orphan note. Offsets sum to less than note duration.
    '''

    note = Note("c'4")
    note = select(note)

    result = mutate(note).split(
        [(1, 32), (5, 32)],
        cyclic=False,
        fracture_spanners=True,
        tie_split_notes=False,
        )

    notes = sequencetools.flatten_sequence(result)
    staff = Staff(notes)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'32
            c'8 ~
            c'32
            c'16
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_25():
    r'''Force splits note in score. Fracture spanners.
    '''

    staff = Staff("c'8 [ ]")

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [ ]
        }
        '''
        ), format(staff)

    notes = staff[:]
    result = mutate(notes).split(
        [Duration(1, 64), Duration(5, 64)],
        cyclic=False,
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'64 [ ]
            c'16 ~ [
            c'64 ]
            c'32 [ ]
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_split_26():
    r'''Splits tuplet in score and do not fracture spanners.
    '''

    voice = Voice()
    voice.append(Tuplet((2, 3), "c'8 d'8 e'8"))
    voice.append(Tuplet((2, 3), "f'8 g'8 a'8"))
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    tuplets = voice[1:2]
    result = mutate(tuplets).split(
        [Duration(1, 12)],
        fracture_spanners=False,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                f'8
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                g'8
                a'8 ]
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_split_27():
    r'''Splits in-score measure with power-of-two denominator and
    do not fracture spanners.
    '''

    voice = Voice()
    voice.append(Measure((3, 8), "c'8 d'8 e'8"))
    voice.append(Measure((3, 8), "f'8 g'8 a'8"))
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    measures = voice[1:2]
    result = mutate(measures).split(
        [Duration(1, 8)],
        fracture_spanners=False,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 3/8
                c'8 [
                d'8
                e'8
            }
            {
                \time 1/8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8 ]
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_split_28():
    r'''Splits in-score measure without power-of-two denominator
    and do not frature spanners.
    '''

    voice = Voice()
    voice.append(Measure((3, 9), "c'8 d'8 e'8", implicit_scaling=True))
    voice.append(Measure((3, 9), "f'8 g'8 a'8", implicit_scaling=True))
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    measures = voice[1:2]
    result = mutate(measures).split(
        [Duration(1, 9)],
        fracture_spanners=False,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 3/9
                \scaleDurations #'(8 . 9) {
                    c'8 [
                    d'8
                    e'8
                }
            }
            {
                \time 1/9
                \scaleDurations #'(8 . 9) {
                    f'8
                }
            }
            {
                \time 2/9
                \scaleDurations #'(8 . 9) {
                    g'8
                    a'8 ]
                }
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_split_29():
    r'''A single container can be splits in the middle.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")

    result = mutate([voice]).split(
        [Duration(1, 4)],
        fracture_spanners=False,
        )

    assert not len(voice)

    voice_1 = result[0][0]
    voice_2 = result[1][0]

    assert format(voice_1) == stringtools.normalize(
        r'''
        \new Voice {
            c'8
            d'8
        }
        '''
        ), format(voice_1)

    assert inspect_(voice_1).is_well_formed()

    assert format(voice_2) == stringtools.normalize(
        r'''
        \new Voice {
            e'8
            f'8
        }
        '''
        ), format(voice_2)

    assert inspect_(voice_2).is_well_formed()


def test_agenttools_MutationAgent_split_30():
    r'''Splits voice at negative index.
    '''

    staff = Staff([Voice("c'8 d'8 e'8 f'8")])
    voice = staff[0]

    result = mutate([voice]).split(
        [Duration(1, 4)],
        fracture_spanners=False,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(left) == stringtools.normalize(
        r'''
        \new Voice {
            c'8
            d'8
        }
        '''
        ), format(left)

    assert format(right) == stringtools.normalize(
        r'''
        \new Voice {
            e'8
            f'8
        }
        '''
        ), format(right)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
        }
        '''
        ), format(voice)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \new Voice {
                c'8
                d'8
            }
            \new Voice {
                e'8
                f'8
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_split_31():
    r'''Slpit container in score and do not fracture spanners.
    '''

    staff = Staff([Container("c'8 d'8 e'8 f'8")])
    voice = staff[0]
    leaves = select(staff).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    result = mutate([voice]).split(
        [Duration(1, 4)],
        fracture_spanners=False,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8 ]
            }
        }
        '''
        ), format(staff)

    assert format(left) == stringtools.normalize(
        r'''
        {
            c'8 [
            d'8
        }
        '''
        ), format(left)

    assert format(right) == stringtools.normalize(
        r'''
        {
            e'8
            f'8 ]
        }
        '''
        ), format(right)

    assert format(voice) == stringtools.normalize(
        r'''
        {
        }
        '''
        ), format(voice)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8 ]
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_split_32():
    r'''Splits tuplet in score and do not fracture spanners.
    '''

    tuplet = Tuplet((4, 5), "c'8 c'8 c'8 c'8 c'8")
    voice = Voice([tuplet])
    staff = Staff([voice])
    beam = Beam()
    attach(beam, tuplet[:])

    result = mutate([tuplet]).split(
        [Duration(1, 5)],
        fracture_spanners=False,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(left) == stringtools.normalize(
        r'''
        \tweak edge-height #'(0.7 . 0)
        \times 4/5 {
            c'8 [
            c'8
        }
        '''
        ), format(left)

    assert format(right) == stringtools.normalize(
        r'''
        \tweak edge-height #'(0.7 . 0)
        \times 4/5 {
            c'8
            c'8
            c'8 ]
        }
        '''
        ), format(right)

    assert format(tuplet) == stringtools.normalize(
        r'''
        \times 4/5 {
        }
        '''
        ), format(tuplet)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \tweak edge-height #'(0.7 . 0)
            \times 4/5 {
                c'8 [
                c'8
            }
            \tweak edge-height #'(0.7 . 0)
            \times 4/5 {
                c'8
                c'8
                c'8 ]
            }
        }
        '''
        ), format(voice)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \new Voice {
                \tweak edge-height #'(0.7 . 0)
                \times 4/5 {
                    c'8 [
                    c'8
                }
                \tweak edge-height #'(0.7 . 0)
                \times 4/5 {
                    c'8
                    c'8
                    c'8 ]
                }
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_split_33():
    r'''Splits triplet, and fracture spanners.
    '''

    voice = Voice()
    voice.append(Tuplet((2, 3), "c'8 d'8 e'8"))
    voice.append(Tuplet((2, 3), "f'8 g'8 a'8"))
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    tuplet = voice[1]

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8 ]
            }
        }
        '''
        ), format(voice)

    result = mutate([tuplet]).split(
        [Duration(1, 12)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(left) == stringtools.normalize(
        r'''
        \tweak edge-height #'(0.7 . 0)
        \times 2/3 {
            f'8 ]
        }
        '''
        ), format(left)

    assert format(right) == stringtools.normalize(
        r'''
        \tweak edge-height #'(0.7 . 0)
        \times 2/3 {
            g'8 [
            a'8 ]
        }
        '''
        ), format(right)

    assert format(tuplet) == '\\times 2/3 {\n}'

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                f'8 ]
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                g'8 [
                a'8 ]
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_split_34():
    r'''Splits measure with power-of-two time signature denominator.
    Fracture spanners.
    '''

    voice = Voice()
    voice.append(Measure((3, 8), "c'8 d'8 e'8"))
    voice.append(Measure((3, 8), "f'8 g'8 a'8"))
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    measure = voice[1]

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 3/8
                c'8 [
                d'8
                e'8
            }
            {
                f'8
                g'8
                a'8 ]
            }
        }
        '''
        ), format(voice)

    result = mutate([measure]).split(
        [Duration(1, 8)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(left) == stringtools.normalize(
        r'''
        {
            \time 1/8
            f'8 ]
        }
        '''
        ), format(left)

    assert format(right) == stringtools.normalize(
        r'''
        {
            \time 2/8
            g'8 [
            a'8 ]
        }
        '''
        ), format(right)

    assert pytest.raises(UnderfullContainerError, 'format(measure)')

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 3/8
                c'8 [
                d'8
                e'8
            }
            {
                \time 1/8
                f'8 ]
            }
            {
                \time 2/8
                g'8 [
                a'8 ]
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_split_35():
    r'''Splits measure without power-of-two time signature denominator.
    Fractures spanners.
    '''

    voice = Voice()
    measure = Measure((3, 9), "c'8 d'8 e'8", implicit_scaling=True)
    voice.append(measure)
    measure = Measure((3, 9), "f'8 g'8 a'8", implicit_scaling=True)
    voice.append(measure)
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    measure = voice[1]

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 3/9
                \scaleDurations #'(8 . 9) {
                    c'8 [
                    d'8
                    e'8
                }
            }
            {
                \scaleDurations #'(8 . 9) {
                    f'8
                    g'8
                    a'8 ]
                }
            }
        }
        '''
        ), format(voice)

    result = mutate([measure]).split(
        [Duration(1, 9)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(left) == stringtools.normalize(
        r'''
        {
            \time 1/9
            \scaleDurations #'(8 . 9) {
                f'8 ]
            }
        }
        '''
        ), format(left)

    assert format(right) == stringtools.normalize(
        r'''
        {
            \time 2/9
            \scaleDurations #'(8 . 9) {
                g'8 [
                a'8 ]
            }
        }
        '''
        ), format(right)

    assert pytest.raises(UnderfullContainerError, 'format(measure)')

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 3/9
                \scaleDurations #'(8 . 9) {
                    c'8 [
                    d'8
                    e'8
                }
            }
            {
                \time 1/9
                \scaleDurations #'(8 . 9) {
                    f'8 ]
                }
            }
            {
                \time 2/9
                \scaleDurations #'(8 . 9) {
                    g'8 [
                    a'8 ]
                }
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_split_36():
    r'''Splits voice outside of score.
    Fracture spanners.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        ), format(voice)

    result = mutate([voice]).split(
        [Duration(1, 4)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(left) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        ), format(left)

    assert format(right) == stringtools.normalize(
        r'''
        \new Voice {
            e'8 [
            f'8 ]
        }
        '''
        ), format(right)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
        }
        '''
        ), format(voice)


def test_agenttools_MutationAgent_split_37():
    r'''Splits measure in score and fracture spanners.
    '''

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    leaves = select(staff).by_leaf()
    beam = Beam()
    attach(beam, leaves[:2])
    beam = Beam()
    attach(beam, leaves[-2:])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(1, 8)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 1/8
                c'8 [ ]
            }
            {
                d'8 [ ] (
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_split_38():
    r'''Splits in-score measure with power-of-two time signature denominator.
    Fractured spanners but do not tie over splits locus.
    Measure contents necessitate denominator change.
    '''

    staff = Staff([Measure((3, 8), "c'8. d'8.")])
    leaves = select(staff).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/8
                c'8. [ (
                d'8. ] )
            }
        }
        '''
        ), format(staff)

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(3, 16)],
        fracture_spanners=True,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/16
                c'8. [ ]
            }
            {
                d'8. [ ]
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 2


def test_agenttools_MutationAgent_split_39():
    r'''Splits cyclic.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        ), format(voice)

    note = voice[0]
    result = mutate(note).split(
        [Duration(1, 8), Duration(3, 8)],
        cyclic=True,
        fracture_spanners=False,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
            }
            {
                d'8
                e'8
                f'8
            }
            {
                g'8
            }
            {
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_split_40():
    r'''Cyclic 1 splits all elements in container.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        ), format(voice)

    container = voice[0]
    result = mutate(container).split(
        [Duration(1, 8)],
        cyclic=True,
        fracture_spanners=False,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
            }
            {
                d'8
            }
            {
                e'8
            }
            {
                f'8 ] )
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_split_41():
    r'''Splits cyclic.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        ), format(voice)

    container = voice[0]
    result = mutate(container).split(
        [Duration(1, 8), Duration(3, 8)],
        cyclic=True,
        fracture_spanners=True,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ ]
            }
            {
                d'8 [ (
                e'8
                f'8 ] )
            }
            {
                g'8 [ ]
            }
            {
                a'8 [ (
                b'8
                c''8 ] )
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()
    assert len(result) == 4


def test_agenttools_MutationAgent_split_42():
    r'''Cyclic by 1 splits all elements in container.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        ), format(voice)

    container = voice[0]
    result = mutate(container).split(
        [Duration(1, 8)],
        cyclic=True,
        fracture_spanners=True,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ ]
            }
            {
                d'8 [ ]
            }
            {
                e'8 [ ]
            }
            {
                f'8 [ ]
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()
    assert len(result) == 4


def test_agenttools_MutationAgent_split_43():
    r'''Extra durations are ignored.
    Result contains no empty shards.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        ), format(voice)

    container = voice[0]
    result = mutate(container).split(
        5 * [Duration(2, 8)],
        cyclic=True,
        fracture_spanners=True,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8 ] )
            }
            {
                e'8 [ (
                f'8 ] )
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()
    assert len(result) == 2


def test_agenttools_MutationAgent_split_44():
    r'''Empty durations list.
    Expression remains unaltered.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        ), format(voice)

    container = voice[0]
    result = mutate(container).split(
        [],
        cyclic=True,
        fracture_spanners=True,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()
    assert len(result) == 1


def test_agenttools_MutationAgent_split_45():
    r'''Splits one time.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        ), format(voice)

    container = voice[0]
    result = mutate(container).split(
        [Duration(1, 8), Duration(3, 8)],
        cyclic=False,
        fracture_spanners=False,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
            }
            {
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_46():
    r'''Splits one time.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        ), format(voice)

    container = voice[0]
    result = mutate(container).split(
        [Duration(1, 8), Duration(3, 8)],
        cyclic=False,
        fracture_spanners=True,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ ]
            }
            {
                d'8 [ (
                e'8
                f'8 ] )
            }
            {
                g'8 [ (
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_47():
    r'''Extra durations are ignored.
    Result contains no empty shards.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        ), format(voice)

    container = voice[0]
    result = mutate(container).split(
        5 * [Duration(2, 8)],
        cyclic=False,
        fracture_spanners=True,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8 ] )
            }
            {
                e'8 [ (
                f'8 ] )
            }
        }
        '''
        ), format(voice)

    assert inspect_(voice).is_well_formed()
    assert len(result) == 2


def test_agenttools_MutationAgent_split_48():
    r'''Splits leaf at relative offset that is both non-assignable
    and non-power-of-two.
    '''

    staff = Staff("c'4")

    notes = staff[:1]
    result = mutate(notes).split(
        [Duration(5, 24)],
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'4 ~
                c'16 ~
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'16
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()


# container._split_at_index() works here;
# scoretools.split() doesn't work here.
# eventually make scoretools.split() work here.
def test_agenttools_MutationAgent_split_49():
    r'''Splits in-score measure without power-of-two time
    signature denominator. Fractured spanners but do not tie
    over splits locus. Measure contents necessitate denominator change.
    '''
    pytest.skip('TODO: make this work.')

    staff = Staff([Measure((3, 12), "c'8. d'8.")])
    leaves = select(staff).by_leaf()
    beam = Beam()
    attach(beam, staff[0])
    slur = Slur()
    attach(slur, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/12
                \scaleDurations #'(2 . 3) {
                    c'8. [ (
                    d'8. ] )
                }
            }
        }
        '''
        ), format(staff)

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(3, 24)],
        fracture_spanners=True,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/24
                \scaleDurations #'(2 . 3) {
                    c'8. [ ] (
                }
            }
            {
                \scaleDurations #'(2 . 3) {
                    d'8. ) [ ]
                }
            }
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()
    assert len(result) == 2
