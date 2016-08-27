# -*- coding: utf-8 -*-
import pytest
from abjad import *


@pytest.mark.skip()
def test_scoretools_fuse_measures_01():
    r'''Fuse unicorporated measures carrying
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

    new = scoretools.fuse_measures(staff[:])

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

    assert new is not measure_1 and new is not measure_2
    assert len(measure_1) == 0
    assert len(measure_2) == 0
    assert inspect_(new).is_well_formed()


@pytest.mark.skip()
def test_scoretools_fuse_measures_02():
    r'''Fuse measures carrying time signatures with differing
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

    scoretools.fuse_measures(voice[:])

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


@pytest.mark.skip()
def test_scoretools_fuse_measures_03():
    r'''Fuse measures with differing power-of-two denominators.
    Helpers selects minimum of two denominators.
    Beam attaches to container rather than leaves.
    '''

    voice = Voice("abj: | 1/8 c'16 d'16 || 2/16 e'16 f'16 |")
    beam = Beam()
    attach(beam, voice[0])

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

    scoretools.fuse_measures(voice[:])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                c'16
                d'16
                e'16
                f'16
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


@pytest.mark.skip()
def test_scoretools_fuse_measures_04():
    r'''Fuse measures with power-of-two-denominators together with measures
    without power-of-two denominators.
    Helpers selects least common multiple of denominators.
    Beams are OK because they attach to leaves rather than containers.
    '''

    measure_1 = Measure((1, 8), "c'8")
    measure_2 = Measure((1, 12), "d'8")
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

    scoretools.fuse_measures(voice[:])

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


@pytest.mark.skip()
def test_scoretools_fuse_measures_05():
    r'''Fusing empty selection returns none.
    '''

    staff = Staff()
    result = scoretools.fuse_measures(staff[:])
    assert result is None


@pytest.mark.skip()
def test_scoretools_fuse_measures_06():
    r'''Fusing selection of only one measure returns measure unaltered.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")
    staff = Staff([measure])
    new = scoretools.fuse_measures(staff[:])

    assert new is measure


@pytest.mark.skip()
def test_scoretools_fuse_measures_07():
    r'''Fuse three measures.
    '''

    voice = Voice("abj: | 1/8 c'16 d'16 || 1/8 e'16 f'16 || 1/8 g'16 a'16 |")
    leaves = select(voice).by_leaf()
    beam = beam = Beam()
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

    scoretools.fuse_measures(voice[:])

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


@pytest.mark.skip()
def test_scoretools_fuse_measures_08():
    r'''Measure fusion across intervening container boundaries is undefined.
    '''

    container_1 = Container("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    container_2 = Container("abj: | 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    voice = Voice([container_1, container_2])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                {
                    \time 2/8
                    c'8
                    d'8
                }
                {
                    \time 2/8
                    e'8
                    f'8
                }
            }
            {
                {
                    \time 2/8
                    g'8
                    a'8
                }
                {
                    \time 2/8
                    b'8
                    c''8
                }
            }
        }
        '''
        )

    assert pytest.raises(
        AssertionError,
        'scoretools.fuse_measures([voice[0][1], voice[1][0]])',
        )


@pytest.mark.skip()
def test_scoretools_fuse_measures_09():
    r'''Fusing measures with power-of-two denominators
    to measures without power-of-two denominators.
    With change in number of note heads because of non-power-of-two multiplier.
    '''

    staff = Staff()
    staff.append(Measure((9, 80), "c'64 c' c' c' c' c' c' c' c'"))
    staff.append(Measure((2, 16), "c'16 c'"))

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

    new = scoretools.fuse_measures(staff[:])

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
