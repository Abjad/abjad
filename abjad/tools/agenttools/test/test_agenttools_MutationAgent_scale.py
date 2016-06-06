# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_MutationAgent_scale_01():
    r'''Scales leaves by dot-generating multiplier.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    mutate(voice).scale(Multiplier(3, 2))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8.
            d'8.
            e'8.
            f'8.
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_scale_02():
    r'''Scales leaves by tie-generating multiplier.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    mutate(voice).scale(Multiplier(5, 4))

    assert format(voice) == stringtools.normalize(
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

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_scale_03():
    r'''Scales leaves by tuplet-generating multiplier.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    mutate(voice).scale(Multiplier(4, 3))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'4
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'4
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                e'4
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                f'4
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_scale_04():
    r'''Scales leaves by tie- and tuplet-generating multiplier.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    mutate(voice).scale(Multiplier(5, 6))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8 ~
                c'32
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'8 ~
                d'32
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                e'8 ~
                e'32
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                f'8 ~
                f'32
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_scale_05():
    r'''Scales mixed notes and tuplets.
    '''

    voice = Voice("c'8.")
    tuplet = scoretools.FixedDurationTuplet((3, 8), "d'8 e'8 f'8 g'8")
    voice.append(tuplet)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8.
            \tweak text #tuplet-number::calc-fraction-text
            \times 3/4 {
                d'8
                e'8
                f'8
                g'8
            }
        }
        '''
        )

    mutate(voice).scale(Multiplier(2, 3))

    assert format(voice) == stringtools.normalize(
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

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_scale_06():
    r'''Undo scale of 5/4 with scale of 4/5.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    mutate(voice).scale(Multiplier(5, 4))

    assert format(voice) == stringtools.normalize(
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

    mutate(voice).scale(Multiplier(4, 5))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_scale_07():
    r'''Doubles measures.
    '''

    voice = Voice()
    voice.append(Measure((2, 8), "c'8 d'8"))
    voice.append(Measure((2, 8), "e'8 f'8"))

    assert format(voice) == stringtools.normalize(
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

    mutate(voice).scale(Multiplier(2))

    assert format(voice) == stringtools.normalize(
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

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_scale_08():
    r'''Scales measures by 5/4.
    '''

    voice = Voice()
    voice.append(Measure((2, 8), "c'8 d'8"))
    voice.append(Measure((2, 8), "e'8 f'8"))

    assert format(voice) == stringtools.normalize(
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

    mutate(voice).scale(Multiplier(5, 4))

    assert format(voice) == stringtools.normalize(
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

    assert inspect_(voice).is_well_formed()
