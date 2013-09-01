# -*- encoding: utf-8 -*-
from abjad import *


def test_Container_scale_01():
    r'''Scale leaves by dot-generating multiplier.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    voice.scale(Multiplier(3, 2))

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8.
            d'8.
            e'8.
            f'8.
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_Container_scale_02():
    r'''Scale leaves by tie-generating multiplier.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    voice.scale(Multiplier(5, 4))

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 ~
            c'32
            d'8 ~
            d'32
            e'8 ~
            e'32
            f'8 ~
            f'32
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_Container_scale_03():
    r'''Scale leaves by tuplet-generating multiplier.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    voice.scale(Multiplier(4, 3))

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'4
            }
            \times 2/3 {
                d'4
            }
            \times 2/3 {
                e'4
            }
            \times 2/3 {
                f'4
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_Container_scale_04():
    r'''Scale leaves by tie- and tuplet-generating multiplier.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    voice.scale(Multiplier(5, 6))

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 ~
                c'32
            }
            \times 2/3 {
                d'8 ~
                d'32
            }
            \times 2/3 {
                e'8 ~
                e'32
            }
            \times 2/3 {
                f'8 ~
                f'32
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_Container_scale_05():
    r'''Scale mixed notes and tuplets.
    '''

    voice = Voice("c'8.")
    tuplet = tuplettools.FixedDurationTuplet((3, 8), "d'8 e'8 f'8 g'8")
    voice.append(tuplet)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8.
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/4 {
                d'8
                e'8
                f'8
                g'8
            }
        }
        '''
        )

    voice.scale(Multiplier(2, 3))

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8
            {
                d'16
                e'16
                f'16
                g'16
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_Container_scale_06():
    r'''Undo scale of 5/4 with scale of 4/5.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    voice.scale(Multiplier(5, 4))

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 ~
            c'32
            d'8 ~
            d'32
            e'8 ~
            e'32
            f'8 ~
            f'32
        }
        '''
        )

    voice.scale(Multiplier(4, 5))

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_Container_scale_07():
    r'''Double measures.
    '''

    voice = Voice()
    voice.append(Measure((2, 8), "c'8 d'8"))
    voice.append(Measure((2, 8), "e'8 f'8"))

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }
        '''
        )

    voice.scale(Multiplier(2))

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/4
                c'4
                d'4
            }
            {
                e'4
                f'4
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_Container_scale_08():
    r'''Scale measures by 5/4.
    '''

    voice = Voice()
    voice.append(Measure((2, 8), "c'8 d'8"))
    voice.append(Measure((2, 8), "e'8 f'8"))

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }
        '''
        )

    voice.scale(Multiplier(5, 4))

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 20/64
                c'8 ~
                c'32
                d'8 ~
                d'32
            }
            {
                e'8 ~
                e'32
                f'8 ~
                f'32
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()
