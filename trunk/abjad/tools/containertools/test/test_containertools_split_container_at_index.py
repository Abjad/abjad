# -*- encoding: utf-8 -*-
from abjad import *
import py


def test_containertools_split_container_at_index_01():
    r'''Split tuplet in score and do not fracture spanners.
    '''

    voice = Voice()
    voice.append(Tuplet((2, 3), "c'8 d'8 e'8"))
    voice.append(Tuplet((2, 3), "f'8 g'8 a'8"))
    beam = spannertools.BeamSpanner(voice[:])

    componenttools.split_components_by_durations(
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


def test_containertools_split_container_at_index_02():
    r'''Split in-score measure with power-of-two denominator and 
    do not fracture spanners.
    '''

    voice = Voice()
    voice.append(Measure((3, 8), "c'8 d'8 e'8"))
    voice.append(Measure((3, 8), "f'8 g'8 a'8"))
    beam = spannertools.BeamSpanner(voice[:])

    componenttools.split_components_by_durations(
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


def test_containertools_split_container_at_index_03():
    r'''Split in-score measure without power-of-two denominator 
    and do not frature spanners.
    '''

    voice = Voice()
    voice.append(Measure((3, 9), "c'8 d'8 e'8"))
    voice.append(Measure((3, 9), "f'8 g'8 a'8"))
    beam = spannertools.BeamSpanner(voice[:])

    componenttools.split_components_by_durations(
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


def test_containertools_split_container_at_index_04():
    r'''A single container can be index split in two by the middle; no parent.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")

    result = componenttools.split_components_by_durations(
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


def test_containertools_split_container_at_index_05():
    r'''Split voice at negative index.
    '''

    staff = Staff([Voice("c'8 d'8 e'8 f'8")])
    voice = staff[0]

    result = componenttools.split_components_by_durations(
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


def test_containertools_split_container_at_index_06():
    r'''Slpit container in score and do not fracture spanners.
    '''

    staff = Staff([Container("c'8 d'8 e'8 f'8")])
    voice = staff[0]
    spannertools.BeamSpanner(voice)

    result = componenttools.split_components_by_durations(
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


def test_containertools_split_container_at_index_07():
    r'''Split tuplet in score and do not fracture spanners.
    '''

    tuplet = Tuplet((4, 5), "c'8 c'8 c'8 c'8 c'8")
    voice = Voice([tuplet])
    staff = Staff([voice])
    spannertools.BeamSpanner(tuplet)

    result = componenttools.split_components_by_durations(
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


def test_containertools_split_container_at_index_08():
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

    result = componenttools.split_components_by_durations(
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


def test_containertools_split_container_at_index_09():
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

    result = componenttools.split_components_by_durations(
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


def test_containertools_split_container_at_index_10():
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

    result = componenttools.split_components_by_durations(
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


def test_containertools_split_container_at_index_11():
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

    result = componenttools.split_components_by_durations(
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


def test_containertools_split_container_at_index_12():
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

    result = componenttools.split_components_by_durations(
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


# containertools.split_container_at_index() works here;
# componenttools.split_components_by_durations() doesn't work here.
# hook in old function.
def test_containertools_split_container_at_index_13():
    r'''Split in-score measure without power-of-two time signature denominator.
    Fractured spanners but do not tie over split locus.
    Measure contents necessitate denominator change.
    '''
    py.test.skip('TODO: make this work.')

    staff = Staff([Measure((3, 12), "c'8. d'8.")])
    spannertools.BeamSpanner(staff[0])
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
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
        )

    halves = componenttools.split_components_by_durations(
        staff[:1], 
        #1, 
        [Duration(3, 24)],
        fracture_spanners=True,
        )

    assert testtools.compare(
        staff,
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
                    d'8. [ ] )
                }
            }
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert len(halves) == 2



def test_containertools_split_container_at_index_14():
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

    halves = componenttools.split_components_by_durations(
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
