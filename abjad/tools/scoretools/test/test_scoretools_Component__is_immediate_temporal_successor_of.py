# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Component__is_immediate_temporal_successor_of_01():

    voice = Voice("c'8 d'8 e'8 f'8")

    assert voice[0]._is_immediate_temporal_successor_of(voice[1])
    assert voice[1]._is_immediate_temporal_successor_of(voice[2])
    assert voice[2]._is_immediate_temporal_successor_of(voice[3])


def test_scoretools_Component__is_immediate_temporal_successor_of_02():

    staff = Staff("c'8 d'8 e'8 f'8")

    assert staff[0]._is_immediate_temporal_successor_of(staff[1])
    assert staff[1]._is_immediate_temporal_successor_of(staff[2])
    assert staff[2]._is_immediate_temporal_successor_of(staff[3])


def test_scoretools_Component__is_immediate_temporal_successor_of_03():

    container = Container("c'8 d'8 e'8 f'8")

    assert container[0]._is_immediate_temporal_successor_of(container[1])
    assert container[1]._is_immediate_temporal_successor_of(container[2])
    assert container[2]._is_immediate_temporal_successor_of(container[3])


def test_scoretools_Component__is_immediate_temporal_successor_of_04():

    tuplet = Tuplet((2, 3), "c'8 d'8 e'8")

    assert tuplet[0]._is_immediate_temporal_successor_of(tuplet[1])
    assert tuplet[1]._is_immediate_temporal_successor_of(tuplet[2])


def test_scoretools_Component__is_immediate_temporal_successor_of_05():

    voice = Voice("{ c'8 d'8 e'8 f'8 } { g'8 a'8 b'8 c''8 }")

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    assert voice[0]._is_immediate_temporal_successor_of(voice[1])
    assert voice[0]._is_immediate_temporal_successor_of(voice[1][0])
    assert voice[0][-1]._is_immediate_temporal_successor_of(voice[1])
    assert voice[0][-1]._is_immediate_temporal_successor_of(voice[1][0])


def test_scoretools_Component__is_immediate_temporal_successor_of_06():

    voice = Voice(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 e'8 d'8 }")

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                e'8
                d'8
            }
        }
        '''
        )

    assert voice[0]._is_immediate_temporal_successor_of(voice[1])
    assert voice[0]._is_immediate_temporal_successor_of(voice[1][0])
    assert voice[0][-1]._is_immediate_temporal_successor_of(voice[1])
    assert voice[0][-1]._is_immediate_temporal_successor_of(voice[1][0])



def test_scoretools_Component__is_immediate_temporal_successor_of_07():

    staff = Staff([Voice("c'8 d'8 e'8 f'8"), Voice("g'8 a'8 b'8 c''8")])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \new Voice {
                c'8
                d'8
                e'8
                f'8
            }
            \new Voice {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    assert staff[0]._is_immediate_temporal_successor_of(staff[1])
    assert staff[0]._is_immediate_temporal_successor_of(staff[1][0])
    assert staff[0][-1]._is_immediate_temporal_successor_of(staff[1])
    assert staff[0][-1]._is_immediate_temporal_successor_of(staff[1][0])


def test_scoretools_Component__is_immediate_temporal_successor_of_08():

    staff = Staff([Voice("c'8 d'8 e'8 f'8"), Voice("g'8 a'8 b'8 c''8")])
    staff[0].name = 'foo'
    staff[1].name = 'foo'

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \context Voice = "foo" {
                c'8
                d'8
                e'8
                f'8
            }
            \context Voice = "foo" {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    assert staff[0]._is_immediate_temporal_successor_of(staff[1])
    assert staff[0]._is_immediate_temporal_successor_of(staff[1][0])
    assert staff[0][-1]._is_immediate_temporal_successor_of(staff[1])



def test_scoretools_Component__is_immediate_temporal_successor_of_09():

    staff = Staff([Voice("c'8 d'8 e'8 f'8"), Voice("g'8 a'8 b'8 c''8")])
    staff[0].name = 'foo'
    staff[1].name = 'bar'

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \context Voice = "foo" {
                c'8
                d'8
                e'8
                f'8
            }
            \context Voice = "bar" {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    assert staff[0]._is_immediate_temporal_successor_of(staff[1])
    assert staff[0]._is_immediate_temporal_successor_of(staff[1][0])
    assert staff[0][-1]._is_immediate_temporal_successor_of(staff[1])


def test_scoretools_Component__is_immediate_temporal_successor_of_10():

    staff_1 = Staff([Voice("c'8 d'8 e'8 f'8")])
    staff_2 = Staff([Voice("g'8 a'8 b'8 c''8")])
    container = Container([staff_1, staff_2])

    assert format(container) == stringtools.normalize(
        r'''
        {
            \new Staff {
                \new Voice {
                    c'8
                    d'8
                    e'8
                    f'8
                }
            }
            \new Staff {
                \new Voice {
                    g'8
                    a'8
                    b'8
                    c''8
                }
            }
        }
        '''
        )

    assert staff_1._is_immediate_temporal_successor_of(staff_2)
    assert staff_1._is_immediate_temporal_successor_of(staff_2[0])
    assert staff_1._is_immediate_temporal_successor_of(staff_2[0][0])

    assert staff_1[0]._is_immediate_temporal_successor_of(staff_2)
    assert staff_1[0]._is_immediate_temporal_successor_of(staff_2[0])
    assert staff_1[0]._is_immediate_temporal_successor_of(staff_2[0][0])

    assert staff_1[0][-1]._is_immediate_temporal_successor_of(staff_2)
    assert staff_1[0][-1]._is_immediate_temporal_successor_of(staff_2[0])
    assert staff_1[0][-1]._is_immediate_temporal_successor_of(staff_2[0][0])


def test_scoretools_Component__is_immediate_temporal_successor_of_11():

    upper_voice_1 = Voice("c''8 d''8 e''8 f''8")
    upper_voice_2 = Voice("g''8 a''8 b''8 c''8")
    lower_voice_1 = Voice("c'8 d'8 e'8 f'8")
    lower_voice_2 = Voice("g'8 a'8 b'8 c''8")
    staff_1 = Staff([upper_voice_1, lower_voice_1])
    staff_2 = Staff([upper_voice_2, lower_voice_2])
    staff_1.is_simultaneous = True
    staff_2.is_simultaneous = True
    container = Container([staff_1, staff_2])

    assert format(container) == stringtools.normalize(
        r'''
        {
            \new Staff <<
                \new Voice {
                    c''8
                    d''8
                    e''8
                    f''8
                }
                \new Voice {
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>
            \new Staff <<
                \new Voice {
                    g''8
                    a''8
                    b''8
                    c''8
                }
                \new Voice {
                    g'8
                    a'8
                    b'8
                    c''8
                }
            >>
        }
        '''
        )

    assert staff_1._is_immediate_temporal_successor_of(staff_2)
    assert staff_1._is_immediate_temporal_successor_of(staff_2[0])
    assert staff_1._is_immediate_temporal_successor_of(staff_2[0][0])
    assert staff_1._is_immediate_temporal_successor_of(staff_2[1])
    assert staff_1._is_immediate_temporal_successor_of(staff_2[1][0])

    assert staff_1[0]._is_immediate_temporal_successor_of(staff_2)
    assert staff_1[0]._is_immediate_temporal_successor_of(staff_2[0])
    assert staff_1[0]._is_immediate_temporal_successor_of(staff_2[0][0])
    assert staff_1[0]._is_immediate_temporal_successor_of(staff_2[1])
    assert staff_1[0]._is_immediate_temporal_successor_of(staff_2[1][0])

    assert staff_1[0][-1]._is_immediate_temporal_successor_of(staff_2)
    assert staff_1[0][-1]._is_immediate_temporal_successor_of(staff_2[0])
    assert staff_1[0][-1]._is_immediate_temporal_successor_of(staff_2[0][0])
    assert staff_1[0][-1]._is_immediate_temporal_successor_of(staff_2[1])
    assert staff_1[0][-1]._is_immediate_temporal_successor_of(staff_2[1][0])

    assert staff_1[1]._is_immediate_temporal_successor_of(staff_2)
    assert staff_1[1]._is_immediate_temporal_successor_of(staff_2[0])
    assert staff_1[1]._is_immediate_temporal_successor_of(staff_2[0][0])
    assert staff_1[1]._is_immediate_temporal_successor_of(staff_2[1])
    assert staff_1[1]._is_immediate_temporal_successor_of(staff_2[1][0])

    assert staff_1[1][-1]._is_immediate_temporal_successor_of(staff_2)
    assert staff_1[1][-1]._is_immediate_temporal_successor_of(staff_2[0])
    assert staff_1[1][-1]._is_immediate_temporal_successor_of(staff_2[0][0])
    assert staff_1[1][-1]._is_immediate_temporal_successor_of(staff_2[1])
    assert staff_1[1][-1]._is_immediate_temporal_successor_of(staff_2[1][0])


def test_scoretools_Component__is_immediate_temporal_successor_of_12():

    voice = Voice("{ { c'8 d'8 e'8 f'8 } } { { g'8 a'8 b'8 c''8 } }")

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }
            }
            {
                {
                    g'8
                    a'8
                    b'8
                    c''8
                }
            }
        }
        '''
        )

    assert voice[0]._is_immediate_temporal_successor_of(voice[1])
    assert voice[0]._is_immediate_temporal_successor_of(voice[1][0])
    assert voice[0]._is_immediate_temporal_successor_of(voice[1][0][0])

    assert voice[0][0]._is_immediate_temporal_successor_of(voice[1])
    assert voice[0][0]._is_immediate_temporal_successor_of(voice[1][0])
    assert voice[0][0]._is_immediate_temporal_successor_of(voice[1][0][0])

    assert voice[0][0][-1]._is_immediate_temporal_successor_of(voice[1])
    assert voice[0][0][-1]._is_immediate_temporal_successor_of(voice[1][0])
    assert voice[0][0][-1]._is_immediate_temporal_successor_of(voice[1][0][0])
