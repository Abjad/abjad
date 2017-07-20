# -*- coding: utf-8 -*-
import abjad
import pytest


def test_agenttools_MutationAgent_split_01():
    r'''Cyclically splits note in score.
    
    Doesn't fracture spanners.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 8), "c'8 d'8"))
    staff.append(abjad.Measure((2, 8), "e'8 f'8"))
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(notes).split(
        [abjad.Duration(3, 64)],
        cyclic=True,
        fracture_spanners=False,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_02():
    r'''Cyclically splits consecutive notes in score.

    Doesn't fracture spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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

    result = abjad.mutate(leaves).split(
        [abjad.Duration(3, 32)],
        cyclic=True,
        fracture_spanners=False,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_03():
    r'''Cyclically splits measure in score.
    
    Doesn't fracture spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(measures).split(
        [abjad.Duration(3, 32)],
        cyclic=True,
        fracture_spanners=False,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_04():
    r'''Cyclically splits consecutive measures in score.

    Doesn't fracture spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(measures).split(
        [abjad.Duration(3, 32)],
        cyclic=True,
        fracture_spanners=False,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_05():
    r'''Cyclically splits orphan measures.

    Doesn't fracture spanners.
    '''

    measures = [
        abjad.Measure((2, 8), "c'8 d'8"),
        abjad.Measure((2, 8), "e'8 f'8"),
        ]
    leaves = abjad.select(measures).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])

    result = abjad.mutate(measures).split(
        [abjad.Duration(3, 32)],
        cyclic=True,
        fracture_spanners=False,
        tie_split_notes=False,
        )

    music = abjad.Sequence(result).flatten()
    staff = abjad.Staff(music)

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_06():
    r'''Cyclically splits note in score.

    Doesn't fracture spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(notes).split(
        [abjad.Duration(1, 32)],
        cyclic=True,
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 4


def test_agenttools_MutationAgent_split_07():
    r'''Cyclically splits consecutive notes in score.

    Doesn't fracture spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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

    result = abjad.mutate(leaves).split(
        [abjad.Duration(1, 16)],
        cyclic=True,
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 8


def test_agenttools_MutationAgent_split_08():
    r'''Cyclically splits measure in score.

    Doesn't fracture spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(measures).split(
        [abjad.Duration(1, 16)],
        cyclic=True,
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 4


def test_agenttools_MutationAgent_split_09():
    r'''Cyclically splits consecutive measures in score.

    Doesn't fracture spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(measures).split(
        [abjad.Duration(3, 32)],
        cyclic=True,
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_10():
    r'''Cyclically splits note in score.

    Fractures spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(notes).split(
        [abjad.Duration(3, 64)],
        cyclic=True,
        fracture_spanners=True,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_11():
    r'''Cyclically splits consecutive notes in score.

    Fractures spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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

    result = abjad.mutate(leaves).split(
        [abjad.Duration(3, 32)],
        cyclic=True,
        fracture_spanners=True,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_12():
    r'''Cyclically splits measure in score.
    
    Fractures spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(measures).split(
        [abjad.Duration(3, 32)],
        cyclic=True,
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_13():
    r'''Cyclically splits consecutive measures in score.

    Fractures spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(measures).split(
        [abjad.Duration(3, 32)],
        cyclic=True,
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_14():
    r'''Cyclically splits orphan notes.
    '''

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
        ]

    result = abjad.mutate(notes).split(
        [abjad.Duration(3, 32)],
        cyclic=True,
        fracture_spanners=True,
        )

    music = abjad.Sequence(result).flatten()
    staff = abjad.Staff(music)

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_15():
    r'''Cyclically splits orphan measures.

    Fractures spanners.
    '''

    measures = [
        abjad.Measure((2, 8), "c'8 d'8"),
        abjad.Measure((2, 8), "e'8 f'8"),
        ]
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, measures[0][:])
    abjad.attach(beam_2, measures[1][:])

    result = abjad.mutate(measures).split(
        [abjad.Duration(3, 32)],
        cyclic=True,
        fracture_spanners=True,
        tie_split_notes=False,
        )

    music = abjad.Sequence(result).flatten()
    staff = abjad.Staff(music)

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_16():
    r'''Cyclically splits note in score.

    Fractures spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(notes).split(
        [abjad.Duration(1, 32)],
        cyclic=True,
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 4


def test_agenttools_MutationAgent_split_17():
    r'''Cyclically splits consecutive notes in score.

    Fractures spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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

    result = abjad.mutate(leaves).split(
        [abjad.Duration(1, 16)],
        cyclic=True,
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 8


def test_agenttools_MutationAgent_split_18():
    r'''Cyclically splits measure in score.

    Fractures spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(measures).split(
        [abjad.Duration(1, 16)],
        cyclic=True,
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 4


def test_agenttools_MutationAgent_split_19():
    r'''Cyclically splits consecutive measures in score.
    
    Fractures spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(measures).split(
        [abjad.Duration(3, 32)],
        cyclic=True,
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 6


def test_agenttools_MutationAgent_split_20():
    r'''Force-splits measure in score.

    Does not fracture spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(measures).split(
        [abjad.Duration(1, 32), abjad.Duration(3, 32), abjad.Duration(5, 32)],
        cyclic=False,
        fracture_spanners=False,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_21():
    r'''Force-splits consecutive measures in score.

    Does not fracture spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(measures).split(
        [abjad.Duration(1, 32), abjad.Duration(3, 32), abjad.Duration(5, 32)],
        cyclic=False,
        fracture_spanners=False,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 4


def test_agenttools_MutationAgent_split_22():
    r'''Force-splits measure in score.
    
    Fractures spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(measures).split(
        [abjad.Duration(1, 32), abjad.Duration(3, 32), abjad.Duration(5, 32)],
        cyclic=False,
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_23():
    r'''Force-splits consecutive measures in score.
    
    Fractures spanners.
    '''

    staff = abjad.Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = abjad.select(staff).by_leaf()
    beam_1 = abjad.Beam()
    beam_2 = abjad.Beam()
    abjad.attach(beam_1, leaves[:2])
    abjad.attach(beam_2, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(measures).split(
        [abjad.Duration(1, 32), abjad.Duration(3, 32), abjad.Duration(5, 32)],
        cyclic=False,
        fracture_spanners=True,
        tie_split_notes=False)

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 4
    assert format(staff) == abjad.String.normalize(
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
    r'''Force-splits orphan note.
    
    Offsets sum to less than note duration.
    '''

    note = abjad.Note("c'4")
    note = abjad.select(note)

    result = abjad.mutate(note).split(
        [(1, 32), (5, 32)],
        cyclic=False,
        fracture_spanners=True,
        tie_split_notes=False,
        )

    notes = abjad.Sequence(result).flatten()
    staff = abjad.Staff(notes)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'32
            c'8 ~
            c'32
            c'16
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 3


def test_agenttools_MutationAgent_split_25():
    r'''Force-splits note in score.
    
    Fractures spanners.
    '''

    staff = abjad.Staff("c'8 [ ]")

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 [ ]
        }
        '''
        ), format(staff)

    notes = staff[:]
    result = abjad.mutate(notes).split(
        [abjad.Duration(1, 64), abjad.Duration(5, 64)],
        cyclic=False,
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'64 [ ]
            c'16 ~ [
            c'64 ]
            c'32 [ ]
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_agenttools_MutationAgent_split_26():
    r'''Splits tuplet in score
    
    Does not fracture spanners.
    '''

    voice = abjad.Voice()
    voice.append(abjad.Tuplet((2, 3), "c'8 d'8 e'8"))
    voice.append(abjad.Tuplet((2, 3), "f'8 g'8 a'8"))
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    tuplets = voice[1:2]
    result = abjad.mutate(tuplets).split(
        [abjad.Duration(1, 12)],
        fracture_spanners=False,
        )

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()


def test_agenttools_MutationAgent_split_27():
    r'''Splits in-score measure with power-of-two denominator.

    Does not fracture spanners.
    '''

    voice = abjad.Voice()
    voice.append(abjad.Measure((3, 8), "c'8 d'8 e'8"))
    voice.append(abjad.Measure((3, 8), "f'8 g'8 a'8"))
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    measures = voice[1:2]
    result = abjad.mutate(measures).split(
        [abjad.Duration(1, 8)],
        fracture_spanners=False,
        )

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()


def test_agenttools_MutationAgent_split_28():
    r'''Splits in-score measure without power-of-two denominator.

    Does not frature spanners.
    '''

    voice = abjad.Voice()
    voice.append(abjad.Measure((3, 9), "c'8 d'8 e'8", implicit_scaling=True))
    voice.append(abjad.Measure((3, 9), "f'8 g'8 a'8", implicit_scaling=True))
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    measures = voice[1:2]
    result = abjad.mutate(measures).split(
        [abjad.Duration(1, 9)],
        fracture_spanners=False,
        )

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()


def test_agenttools_MutationAgent_split_29():
    r'''Splits container in middle.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")

    result = abjad.mutate([voice]).split(
        [abjad.Duration(1, 4)],
        fracture_spanners=False,
        )

    assert not len(voice)

    voice_1 = result[0][0]
    voice_2 = result[1][0]

    assert format(voice_1) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8
            d'8
        }
        '''
        ), format(voice_1)

    assert abjad.inspect(voice_1).is_well_formed()

    assert format(voice_2) == abjad.String.normalize(
        r'''
        \new Voice {
            e'8
            f'8
        }
        '''
        ), format(voice_2)

    assert abjad.inspect(voice_2).is_well_formed()


def test_agenttools_MutationAgent_split_30():
    r'''Splits voice at negative index.
    '''

    staff = abjad.Staff([abjad.Voice("c'8 d'8 e'8 f'8")])
    voice = staff[0]

    result = abjad.mutate([voice]).split(
        [abjad.Duration(1, 4)],
        fracture_spanners=False,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(left) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8
            d'8
        }
        '''
        ), format(left)

    assert format(right) == abjad.String.normalize(
        r'''
        \new Voice {
            e'8
            f'8
        }
        '''
        ), format(right)

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
        }
        '''
        ), format(voice)

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()


def test_agenttools_MutationAgent_split_31():
    r'''Slpits container in score.
    
    Does not fracture spanners.
    '''

    staff = abjad.Staff([abjad.Container("c'8 d'8 e'8 f'8")])
    voice = staff[0]
    leaves = abjad.select(staff).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    result = abjad.mutate([voice]).split(
        [abjad.Duration(1, 4)],
        fracture_spanners=False,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(staff) == abjad.String.normalize(
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

    assert format(left) == abjad.String.normalize(
        r'''
        {
            c'8 [
            d'8
        }
        '''
        ), format(left)

    assert format(right) == abjad.String.normalize(
        r'''
        {
            e'8
            f'8 ]
        }
        '''
        ), format(right)

    assert format(voice) == abjad.String.normalize(
        r'''
        {
        }
        '''
        ), format(voice)

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()


def test_agenttools_MutationAgent_split_32():
    r'''Splits tuplet in score.
    
    Does not fracture spanners.
    '''

    tuplet = abjad.Tuplet((4, 5), "c'8 c'8 c'8 c'8 c'8")
    voice = abjad.Voice([tuplet])
    staff = abjad.Staff([voice])
    beam = abjad.Beam()
    abjad.attach(beam, tuplet[:])

    result = abjad.mutate([tuplet]).split(
        [abjad.Duration(1, 5)],
        fracture_spanners=False,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(left) == abjad.String.normalize(
        r'''
        \tweak edge-height #'(0.7 . 0)
        \times 4/5 {
            c'8 [
            c'8
        }
        '''
        ), format(left)

    assert format(right) == abjad.String.normalize(
        r'''
        \tweak edge-height #'(0.7 . 0)
        \times 4/5 {
            c'8
            c'8
            c'8 ]
        }
        '''
        ), format(right)

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \times 4/5 {
        }
        '''
        ), format(tuplet)

    assert format(voice) == abjad.String.normalize(
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

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()


def test_agenttools_MutationAgent_split_33():
    r'''Splits tuplet in score
    
    Fractures spanners.
    '''

    voice = abjad.Voice()
    voice.append(abjad.Tuplet((2, 3), "c'8 d'8 e'8"))
    voice.append(abjad.Tuplet((2, 3), "f'8 g'8 a'8"))
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    tuplet = voice[1]

    assert format(voice) == abjad.String.normalize(
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

    result = abjad.mutate([tuplet]).split(
        [abjad.Duration(1, 12)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(left) == abjad.String.normalize(
        r'''
        \tweak edge-height #'(0.7 . 0)
        \times 2/3 {
            f'8 ]
        }
        '''
        ), format(left)

    assert format(right) == abjad.String.normalize(
        r'''
        \tweak edge-height #'(0.7 . 0)
        \times 2/3 {
            g'8 [
            a'8 ]
        }
        '''
        ), format(right)

    assert format(tuplet) == '\\times 2/3 {\n}'

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()


def test_agenttools_MutationAgent_split_34():
    r'''Splits measure with power-of-two time signature denominator.

    Fractures spanners.
    '''

    voice = abjad.Voice()
    voice.append(abjad.Measure((3, 8), "c'8 d'8 e'8"))
    voice.append(abjad.Measure((3, 8), "f'8 g'8 a'8"))
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    measure = voice[1]

    assert format(voice) == abjad.String.normalize(
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

    result = abjad.mutate([measure]).split(
        [abjad.Duration(1, 8)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(left) == abjad.String.normalize(
        r'''
        {
            \time 1/8
            f'8 ]
        }
        '''
        ), format(left)

    assert format(right) == abjad.String.normalize(
        r'''
        {
            \time 2/8
            g'8 [
            a'8 ]
        }
        '''
        ), format(right)

    assert pytest.raises(UnderfullContainerError, 'format(measure)')

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()


def test_agenttools_MutationAgent_split_35():
    r'''Splits measure without power-of-two denominator.

    Fractures spanners.
    '''

    voice = abjad.Voice()
    measure = abjad.Measure((3, 9), "c'8 d'8 e'8", implicit_scaling=True)
    voice.append(measure)
    measure = abjad.Measure((3, 9), "f'8 g'8 a'8", implicit_scaling=True)
    voice.append(measure)
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    measure = voice[1]

    assert format(voice) == abjad.String.normalize(
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

    result = abjad.mutate([measure]).split(
        [abjad.Duration(1, 9)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(left) == abjad.String.normalize(
        r'''
        {
            \time 1/9
            \scaleDurations #'(8 . 9) {
                f'8 ]
            }
        }
        '''
        ), format(left)

    assert format(right) == abjad.String.normalize(
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

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()


def test_agenttools_MutationAgent_split_36():
    r'''Splits voice outside of score.

    Fractures spanners.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        ), format(voice)

    result = abjad.mutate([voice]).split(
        [abjad.Duration(1, 4)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(left) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        ), format(left)

    assert format(right) == abjad.String.normalize(
        r'''
        \new Voice {
            e'8 [
            f'8 ]
        }
        '''
        ), format(right)

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
        }
        '''
        ), format(voice)


def test_agenttools_MutationAgent_split_37():
    r'''Splits measure in score.
    
    Fractures spanners.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 8), "c'8 d'8"))
    staff.append(abjad.Measure((2, 8), "e'8 f'8"))
    leaves = abjad.select(staff).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(measures).split(
        [abjad.Duration(1, 8)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()


def test_agenttools_MutationAgent_split_38():
    r'''Splits in-score measure with power-of-two denominator.

    Fractures spanners but does not tie over split.

    Changes measure denominator.
    '''

    staff = abjad.Staff([abjad.Measure((3, 8), "c'8. d'8.")])
    leaves = abjad.select(staff).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
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
    result = abjad.mutate(measures).split(
        [abjad.Duration(3, 16)],
        fracture_spanners=True,
        )

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 2


def test_agenttools_MutationAgent_split_39():
    r'''Splits cyclically.

    Leave spanner untouched.
    '''

    voice = abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(voice) == abjad.String.normalize(
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
    result = abjad.mutate(note).split(
        [abjad.Duration(1, 8), abjad.Duration(3, 8)],
        cyclic=True,
        fracture_spanners=False,
        )

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()


def test_agenttools_MutationAgent_split_40():
    r'''Cyclically splits all components in container.
    '''

    voice = abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8")])
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(voice) == abjad.String.normalize(
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
    result = abjad.mutate(container).split(
        [abjad.Duration(1, 8)],
        cyclic=True,
        fracture_spanners=False,
        )

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()


def test_agenttools_MutationAgent_split_41():
    r'''Cyclically splits all components in container.
    '''

    voice = abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8")])
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(voice) == abjad.String.normalize(
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
    result = abjad.mutate(container).split(
        [abjad.Duration(1, 8)],
        cyclic=True,
        fracture_spanners=True,
        )

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()
    assert len(result) == 4


def test_agenttools_MutationAgent_split_42():
    r'''Ignores extra durations.

    Result contains no empty shards.
    '''

    voice = abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8")])
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(voice) == abjad.String.normalize(
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
    result = abjad.mutate(container).split(
        5 * [abjad.Duration(2, 8)],
        cyclic=True,
        fracture_spanners=True,
        )

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()
    assert len(result) == 2


def test_agenttools_MutationAgent_split_43():
    r'''Leaves container unchanged because of empty duration list.
    '''

    voice = abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8")])
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(voice) == abjad.String.normalize(
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
    result = abjad.mutate(container).split(
        [],
        cyclic=True,
        fracture_spanners=True,
        )

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()
    assert len(result) == 1


def test_agenttools_MutationAgent_split_44():
    r'''Ignores extra durations.

    Result contains no empty shards.
    '''

    voice = abjad.Voice([abjad.Container("c'8 d'8 e'8 f'8")])
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(voice) == abjad.String.normalize(
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
    result = abjad.mutate(container).split(
        5 * [abjad.Duration(2, 8)],
        cyclic=False,
        fracture_spanners=True,
        )

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()
    assert len(result) == 2


def test_agenttools_MutationAgent_split_45():
    r'''Splits leaf at non-assignable, non-power-of-two offset.
    '''

    staff = abjad.Staff("c'4")

    notes = staff[:1]
    result = abjad.mutate(notes).split(
        [abjad.Duration(5, 24)],
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \times 2/3 {
                c'4 ~
                c'16 ~
                c'16
            }
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_agenttools_MutationAgent_split_46():
    r'''Splits in-score measure without power-of-two denominator.

    Fractures spanners but does not tie over split.
    
    Changes measure denominator.
    '''

    measure = abjad.Measure((3, 12), "c'8. d'8.", implicit_scaling=True)
    staff = abjad.Staff([measure])
    leaves = abjad.select(staff).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            {
                \time 3/12
                \scaleDurations #'(2 . 3) {
                    c'8. [
                    d'8. ]
                }
            }
        }
        '''
        ), format(staff)

    measures = staff[:1]
    result = abjad.mutate(measures).split(
        [abjad.Duration(3, 24)],
        fracture_spanners=True,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            {
                \time 3/24
                \scaleDurations #'(2 . 3) {
                    c'8. [ ]
                }
            }
            {
                \scaleDurations #'(2 . 3) {
                    d'8. [ ]
                }
            }
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 2
