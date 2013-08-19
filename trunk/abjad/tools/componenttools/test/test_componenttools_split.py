# -*- encoding: utf-8 -*-
import py
from abjad import *


def test_componenttools_split_01():
    r'''Cyclically split note in score. Don't fracture spanners.
    '''

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[0][1:2], 
        [Duration(3, 64)],
        cyclic=True,
        fracture_spanners=False,
        )

    assert testtools.compare(
        staff,
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
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 3


def test_componenttools_split_02():
    r'''Cyclically split consecutive notes in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff.select_leaves(), 
        [Duration(3, 32)], 
        cyclic=True,
        fracture_spanners=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'16. [ ( ~
                c'32
                d'16 ~
                d'16 ]
            }
            {
                e'32 [ ~
                e'16.
                f'16. ~
                f'32 ] )
            }
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 6


def test_componenttools_split_03():
    r'''Cyclically split measure in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[:1], 
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=False, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
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
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 3


def test_componenttools_split_04():
    r'''Cyclically split consecutive measures in score. 
    Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[:], 
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=False, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
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
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 6


def test_componenttools_split_05():
    r'''Cyclically split orphan measures. Don't fracture spanners.
    '''

    measures = [Measure((2, 8), "c'8 d'8"), Measure((2, 8), "e'8 f'8")]
    select(measures).attach_spanners(spannertools.BeamSpanner)

    parts = componenttools.split(
        measures, 
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=False, 
        tie_split_notes=False,
        )

    music = sequencetools.flatten_sequence(parts)
    staff = Staff(music)

    assert testtools.compare(
        staff,
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
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 6


def test_componenttools_split_06():
    r'''Cyclically split note in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[0][1:], 
        [Duration(1, 32)],
        cyclic=True, 
        fracture_spanners=False, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
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
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 4


def test_componenttools_split_07():
    r'''Cyclically split consecutive notes in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff.select_leaves(), 
        [Duration(1, 16)],
        cyclic=True, 
        fracture_spanners=False, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'16 [ ( ~
                c'16
                d'16 ~
                d'16 ]
            }
            {
                e'16 [ ~
                e'16
                f'16 ~
                f'16 ] )
            }
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 8


def test_componenttools_split_08():
    r'''Cyclically split measure in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[:1], 
        [Duration(1, 16)],
        cyclic=True, 
        fracture_spanners=False, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/16
                c'16 [ ( ~
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
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 4


def test_componenttools_split_09():
    r'''Cyclically split consecutive measures in score. 
    Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[:], 
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=False, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ ( ~
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
                e'32 [ ~
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
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 6


def test_componenttools_split_10():
    r'''Cyclically split note in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[0][1:2], 
        [Duration(3, 64)], 
        cyclic=True,
        fracture_spanners=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'32. ) ~
                d'32. ( ) ~
                d'32 ] (
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 3


def test_componenttools_split_11():
    r'''Cyclically split consecutive notes in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff.select_leaves(), 
        [Duration(3, 32)], 
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'16. [ ( ) ~
                c'32 (
                d'16 ) ~
                d'16 ] (
            }
            {
                e'32 [ ) ~
                e'16. (
                f'16. ) ~
                f'32 ] ( )
            }
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 6


def test_componenttools_split_12():
    r'''Cyclically split measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[:1], 
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=True, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ ] ( )
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
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 3


def test_componenttools_split_13():
    r'''Cyclically split consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[:], 
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=True, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ ] ( )
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
                e'32 [ ] )
            }
            {
                \time 3/32
                e'16. [ ] ( )
            }
            {
                f'16. [ ] ( )
            }
            {
                \time 1/32
                f'32 [ ] ( )
            }
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 6


def test_componenttools_split_14():
    r'''Cyclically split orphan notes.
    '''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]

    parts = componenttools.split(
        notes, 
        [Duration(3, 32)], 
        cyclic=True, 
        fracture_spanners=True,
        )

    music = sequencetools.flatten_sequence(parts)
    staff = Staff(music)

    assert testtools.compare(
        staff,
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
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 6


def test_componenttools_split_15():
    r'''Cyclically split orphan measures. Fracture spanners.
    '''

    measures = [Measure((2, 8), "c'8 d'8"), Measure((2, 8), "e'8 f'8")]
    select(measures).attach_spanners(spannertools.BeamSpanner)

    parts = componenttools.split(
        measures, 
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=True, 
        tie_split_notes=False,
        )

    music = sequencetools.flatten_sequence(parts)
    staff = Staff(music)

    assert testtools.compare(
        staff,
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
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 6


def test_componenttools_split_16():
    r'''Cyclically split note in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[0][1:], 
        [Duration(1, 32)],
        cyclic=True, 
        fracture_spanners=True, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'32 ) ~
                d'32 ( ) ~
                d'32 ( ) ~
                d'32 ] (
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 4


def test_componenttools_split_17():
    r'''Cyclically split consecutive notes in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff.select_leaves(), 
        [Duration(1, 16)],
        cyclic=True, 
        fracture_spanners=True, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'16 [ ( ) ~
                c'16 (
                d'16 ) ~
                d'16 ] (
            }
            {
                e'16 [ ) ~
                e'16 (
                f'16 ) ~
                f'16 ] ( )
            }
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 8


def test_componenttools_split_18():
    r'''Cyclically split measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[:1], 
        [Duration(1, 16)],
        cyclic=True, 
        fracture_spanners=True, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/16
                c'16 [ ] ( ) ~
            }
            {
                c'16 [ ] ( )
            }
            {
                d'16 [ ] ( ) ~
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
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 4


def test_componenttools_split_19():
    r'''Cyclically split consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[:], 
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=True, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ ] ( ) ~
            }
            {
                c'32 [ (
                d'16 ] ) ~
            }
            {
                \time 2/32
                d'16 [ ] (
            }
            {
                \time 1/32
                e'32 [ ] ) ~
            }
            {
                \time 3/32
                e'16. [ ] ( )
            }
            {
                f'16. [ ] ( ) ~
            }
            {
                \time 1/32
                f'32 [ ] ( )
            }
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 6


def test_componenttools_split_20():
    r'''Force split measure in score. Do not fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[:1], 
        [Duration(1, 32), Duration(3, 32), Duration(5, 32)],
        cyclic=False, 
        fracture_spanners=False, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
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
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 3


def test_componenttools_split_21():
    r'''Force split consecutive measures in score. Do not fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[:], 
        [Duration(1, 32), Duration(3, 32), Duration(5, 32)],
        cyclic=False, 
        fracture_spanners=False, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
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
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 4


def test_componenttools_split_22():
    r'''Force split measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[:1], 
        [Duration(1, 32), Duration(3, 32), Duration(5, 32)],
        cyclic=False, 
        fracture_spanners=True, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/32
                c'32 [ ] ( )
            }
            {
                \time 3/32
                c'16. [ ] ( )
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
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 3


def test_componenttools_split_23():
    r'''Force split consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    parts = componenttools.split(
        staff[:], 
        [Duration(1, 32), Duration(3, 32), Duration(5, 32)],
        cyclic=False, 
        fracture_spanners=True, 
        tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ ] ( )
        }
        {
            \time 3/32
            c'16. [ ] ( )
        }
        {
            \time 4/32
            d'8 [ ] (
        }
        {
            \time 1/32
            e'32 [ ] )
        }
        {
            \time 7/32
            e'16. [ (
            f'8 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 4
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/32
                c'32 [ ] ( )
            }
            {
                \time 3/32
                c'16. [ ] ( )
            }
            {
                \time 4/32
                d'8 [ ] (
            }
            {
                \time 1/32
                e'32 [ ] )
            }
            {
                \time 7/32
                e'16. [ (
                f'8 ] )
            }
        }
        '''
        )


def test_componenttools_split_24():
    r'''Force split orphan note. Offsets sum to less than note duration.
    '''

    note = Note("c'4")

    parts = componenttools.split(
        [note], 
        [(1, 32), (5, 32)],
        cyclic=False, 
        fracture_spanners=True, 
        tie_split_notes=False,
        )

    notes = sequencetools.flatten_sequence(parts)
    staff = Staff(notes)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'32
            c'8 ~
            c'32
            c'16
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert len(parts) == 3


def test_componenttools_split_25():
    r'''Force split note in score. Fracture spanners.
    '''

    staff = Staff("c'8 [ ]")

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [ ]
        }
        '''
        )

    parts = componenttools.split(
        staff[:], 
        [Duration(1, 64), Duration(5, 64)],
        cyclic=False, 
        fracture_spanners=True, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'64 [ ]
            c'16 [ ~
            c'64 ]
            c'32 [ ]
        }
        '''
        )

    assert select(staff).is_well_formed()


def test_componenttools_split_26():
    r'''Split tuplet in score and do not fracture spanners.
    '''

    voice = Voice()
    voice.append(Tuplet((2, 3), "c'8 d'8 e'8"))
    voice.append(Tuplet((2, 3), "f'8 g'8 a'8"))
    beam = spannertools.BeamSpanner(voice[:])

    componenttools.split(
        voice[1:2],
        [Duration(1, 12)],
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                f'8
            }
            \times 2/3 {
                g'8
                a'8 ]
            }
        }
        '''
        )

    assert select(voice).is_well_formed()


def test_componenttools_split_27():
    r'''Split in-score measure with power-of-two denominator and 
    do not fracture spanners.
    '''

    voice = Voice()
    voice.append(Measure((3, 8), "c'8 d'8 e'8"))
    voice.append(Measure((3, 8), "f'8 g'8 a'8"))
    beam = spannertools.BeamSpanner(voice[:])

    componenttools.split(
        voice[1:2], 
        [Duration(1, 8)], 
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
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
        )

    assert select(voice).is_well_formed()


def test_componenttools_split_28():
    r'''Split in-score measure without power-of-two denominator 
    and do not frature spanners.
    '''

    voice = Voice()
    voice.append(Measure((3, 9), "c'8 d'8 e'8"))
    voice.append(Measure((3, 9), "f'8 g'8 a'8"))
    beam = spannertools.BeamSpanner(voice[:])

    componenttools.split(
        voice[1:2], 
        [Duration(1, 9)], 
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
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
        )

    assert select(voice).is_well_formed()


def test_componenttools_split_29():
    r'''A single container can be index split in two by the middle; no parent.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")

    result = componenttools.split(
        [voice], 
        [Duration(1, 4)], 
        fracture_spanners=False,
        )

    assert select(voice).is_well_formed()

    voice_1 = result[0][0]
    voice_2 = result[1][0]

    assert testtools.compare(
        voice_1,
        r'''
        \new Voice {
            c'8
            d'8
        }
        '''
        )

    assert select(voice_1).is_well_formed()

    assert testtools.compare(
        voice_2,
        r'''
        \new Voice {
            e'8
            f'8
        }
        '''
        )

    assert select(voice_2).is_well_formed()


def test_componenttools_split_30():
    r'''Split voice at negative index.
    '''

    staff = Staff([Voice("c'8 d'8 e'8 f'8")])
    voice = staff[0]

    result = componenttools.split(
        [voice], 
        #-2, 
        [Duration(1, 4)],
        fracture_spanners=False,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        left,
        r'''
        \new Voice {
            c'8
            d'8
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        \new Voice {
            e'8
            f'8
        }
        '''
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
        }
        '''
        )

    assert testtools.compare(
        staff,
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
        )

    assert select(staff).is_well_formed()


def test_componenttools_split_31():
    r'''Slpit container in score and do not fracture spanners.
    '''

    staff = Staff([Container("c'8 d'8 e'8 f'8")])
    voice = staff[0]
    spannertools.BeamSpanner(voice)

    result = componenttools.split(
        [voice], 
        #2, 
        [Duration(1, 4)],
        fracture_spanners=False,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        staff,
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
        )

    assert testtools.compare(
        left,
        r'''
        {
            c'8 [
            d'8
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        {
            e'8
            f'8 ]
        }
        '''
        )

    assert testtools.compare(
        voice,
        r'''
        {
        }
        '''
        )

    assert testtools.compare(
        staff,
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
        )

    assert select(staff).is_well_formed()


def test_componenttools_split_32():
    r'''Split tuplet in score and do not fracture spanners.
    '''

    tuplet = Tuplet((4, 5), "c'8 c'8 c'8 c'8 c'8")
    voice = Voice([tuplet])
    staff = Staff([voice])
    spannertools.BeamSpanner(tuplet)

    result = componenttools.split(
        [tuplet], 
        #2, 
        [Duration(1, 5)],
        fracture_spanners=False,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \new Voice {
                \times 4/5 {
                    c'8 [
                    c'8
                }
                \times 4/5 {
                    c'8
                    c'8
                    c'8 ]
                }
            }
        }
        '''
        )

    assert testtools.compare(
        left,
        r'''
        \times 4/5 {
            c'8 [
            c'8
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        \times 4/5 {
            c'8
            c'8
            c'8 ]
        }
        '''
        )

    assert testtools.compare(
        tuplet,
        r'''
        \times 4/5 {
        }
        '''
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 4/5 {
                c'8 [
                c'8
            }
            \times 4/5 {
                c'8
                c'8
                c'8 ]
            }
        }
        '''
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \new Voice {
                \times 4/5 {
                    c'8 [
                    c'8
                }
                \times 4/5 {
                    c'8
                    c'8
                    c'8 ]
                }
            }
        }
        '''
        )

    assert select(staff).is_well_formed()


def test_componenttools_split_33():
    r'''Split triplet, and fracture spanners.
    '''

    voice = Voice()
    voice.append(Tuplet((2, 3), "c'8 d'8 e'8"))
    voice.append(Tuplet((2, 3), "f'8 g'8 a'8"))
    spannertools.BeamSpanner(voice[:])
    tuplet = voice[1]

    assert testtools.compare(
        voice,
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
        )

    result = componenttools.split(
        [tuplet], 
        #1, 
        [Duration(1, 12)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        left,
        r'''
        \times 2/3 {
            f'8 ]
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        \times 2/3 {
            g'8 [
            a'8 ]
        }
        '''
        )

    assert tuplet.lilypond_format == '\\times 2/3 {\n}'

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                f'8 ]
            }
            \times 2/3 {
                g'8 [
                a'8 ]
            }
        }
        '''
        )

    assert select(voice).is_well_formed()


def test_componenttools_split_34():
    r'''Split measure with power-of-two time signature denominator.
    Fracture spanners.
    '''

    voice = Voice()
    voice.append(Measure((3, 8), "c'8 d'8 e'8"))
    voice.append(Measure((3, 8), "f'8 g'8 a'8"))
    spannertools.BeamSpanner(voice[:])
    measure = voice[1]

    assert testtools.compare(
        voice,
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
        )

    result = componenttools.split(
        [measure], 
        #1, 
        [Duration(1, 8)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        left,
        r'''
        {
            \time 1/8
            f'8 ]
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        {
            \time 2/8
            g'8 [
            a'8 ]
        }
        '''
        )

    assert py.test.raises(UnderfullContainerError, 'measure.lilypond_format')

    assert testtools.compare(
        voice,
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
        )

    assert select(voice).is_well_formed()


def test_componenttools_split_35():
    r'''Split measure without power-of-two time signature denominator.
    Fracture spanners.
    '''

    voice = Voice()
    voice.append(Measure((3, 9), "c'8 d'8 e'8"))
    voice.append(Measure((3, 9), "f'8 g'8 a'8"))
    spannertools.BeamSpanner(voice[:])
    measure = voice[1]

    assert testtools.compare(
        voice,
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
        )

    result = componenttools.split(
        [measure], 
        #1, 
        [Duration(1, 9)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        left,
        r'''
        {
            \time 1/9
            \scaleDurations #'(8 . 9) {
                f'8 ]
            }
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        {
            \time 2/9
            \scaleDurations #'(8 . 9) {
                g'8 [
                a'8 ]
            }
        }
        '''
        )

    assert py.test.raises(UnderfullContainerError, 'measure.lilypond_format')

    assert testtools.compare(
        voice,
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
        )

    assert select(voice).is_well_formed()


def test_componenttools_split_36():
    r'''Split voice outside of score.
    Fracture spanners.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    result = componenttools.split(
        [voice], 
        #2, 
        [Duration(1, 4)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        left,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        \new Voice {
            e'8 [
            f'8 ]
        }
        '''
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
        }
        '''
        )


def test_componenttools_split_37():
    r'''Split measure in score and fracture spanners.
    '''

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    spannertools.BeamSpanner(staff[0])
    spannertools.BeamSpanner(staff[1])
    slur = spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    result = componenttools.split(
        staff[:1], 
        #1, 
        [Duration(1, 8)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/8
                c'8 [ ] ( )
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
        )

    assert select(staff).is_well_formed()





def test_componenttools_split_38():
    r'''Split in-score measure with power-of-two time signature denominator.
    Fractured spanners but do not tie over split locus.
    Measure contents necessitate denominator change.
    '''

    staff = Staff([Measure((3, 8), "c'8. d'8.")])
    spannertools.BeamSpanner(staff[0])
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/8
                c'8. [ (
                d'8. ] )
            }
        }
        '''
        )

    halves = componenttools.split(
        staff[:1], 
        #1, 
        [Duration(3, 16)],
        fracture_spanners=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/16
                c'8. [ ] ( )
            }
            {
                d'8. [ ] ( )
            }
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert len(halves) == 2


def test_componenttools_split_39():
    r'''Partition container into parts of lengths equal to counts.
    Read list of counts cyclically.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
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
        )

    componenttools.split(
        voice[0], 
        #[1, 3], 
        [Duration(1, 8), Duration(3, 8)],
        cyclic=True, 
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
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
        )

    assert select(voice).is_well_formed()


def test_componenttools_split_40():
    r'''Cyclic 1 splits all elements in container.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
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
        )

    componenttools.split(
        voice[0], 
        #[1], 
        [Duration(1, 8)],
        cyclic=True, 
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
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
        )

    assert select(voice).is_well_formed()


def test_componenttools_split_41():
    r'''Partition container into parts of lengths equal to counts.
    Read list of counts cyclically.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
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
        )

    result = componenttools.split(
        voice[0], 
        #[1, 3], 
        [Duration(1, 8), Duration(3, 8)],
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ ] ( )
            }
            {
                d'8 [ (
                e'8
                f'8 ] )
            }
            {
                g'8 [ ] ( )
            }
            {
                a'8 [ (
                b'8
                c''8 ] )
            }
        }
        '''
        )

    assert select(voice).is_well_formed()
    assert len(result) == 4


def test_componenttools_split_42():
    r'''Cyclic by 1 splits all elements in container.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
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
        )

    result = componenttools.split(
        voice[0], 
        #[1], 
        [Duration(1, 8)],
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ ] ( )
            }
            {
                d'8 [ ] ( )
            }
            {
                e'8 [ ] ( )
            }
            {
                f'8 [ ] ( )
            }
        }
        '''
        )

    assert select(voice).is_well_formed()
    assert len(result) == 4


def test_componenttools_split_43():
    r'''Partition by large number of part counts.
    First part counts apply and extra part counts do not apply.
    Result contains no empty parts.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
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
        )

    result = componenttools.split(
        voice[0], 
        5 * [Duration(2, 8)],
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
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
        )

    assert select(voice).is_well_formed()
    assert len(result) == 2


def test_componenttools_split_44():
    r'''Partition by large empty part counts list.
    Expression remains unaltered.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
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
        )

    result = componenttools.split(
        voice[0], 
        [], 
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
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
        )

    assert select(voice).is_well_formed()
    assert len(result) == 2


def test_componenttools_split_45():
    r'''Partition container into parts of lengths equal to counts.
    Read list of counts only once; do not cycle.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
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
        )

    result = componenttools.split(
        voice[0], 
        #[1, 3], 
        [Duration(1, 8), Duration(3, 8)],
        cyclic=False, 
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
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
        )

    assert select(voice).is_well_formed()
    assert len(result) == 3


def test_componenttools_split_46():
    r'''Partition container into parts of lengths equal to counts.
    Read list of counts only once; do not cycle.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
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
        )

    result = componenttools.split(
        voice[0], 
        #[1, 3], 
        [Duration(1, 8), Duration(3, 8)],
        cyclic=False, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ ] ( )
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
        )

    assert select(voice).is_well_formed()
    assert len(result) == 3


def test_componenttools_split_47():
    r'''Partition by large number of part counts.
    First part counts apply and extra part counts do not apply.
    Result contains no empty parts.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
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
        )

    result = componenttools.split(
        voice[0], 
        5 * [Duration(2, 8)],
        cyclic=False, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
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
        )

    assert select(voice).is_well_formed()
    assert len(result) == 2
