# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_Selection__get_component_01():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    assert select(staff)._get_component(Measure, 0) is staff[0]
    assert select(staff)._get_component(Measure, 1) is staff[1]
    assert select(staff)._get_component(Measure, 2) is staff[2]


def test_selectiontools_Selection__get_component_02():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    assert select(staff)._get_component(Measure, -1) is staff[2]
    assert select(staff)._get_component(Measure, -2) is staff[1]
    assert select(staff)._get_component(Measure, -3) is staff[0]


def test_selectiontools_Selection__get_component_03():
    r'''Read forwards for positive n.
    '''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    r'''
    \new Staff {
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
      {
            \time 2/8
            g'8
            a'8
      }
    }
    '''

    assert select(staff)._get_component(scoretools.Leaf, 0) is staff[0][0]
    assert select(staff)._get_component(scoretools.Leaf, 1) is staff[0][1]
    assert select(staff)._get_component(scoretools.Leaf, 2) is staff[1][0]
    assert select(staff)._get_component(scoretools.Leaf, 3) is staff[1][1]
    assert select(staff)._get_component(scoretools.Leaf, 4) is staff[2][0]
    assert select(staff)._get_component(scoretools.Leaf, 5) is staff[2][1]


def test_selectiontools_Selection__get_component_04():
    r'''Read backwards for negative n.
    '''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    r'''
    \new Staff {
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
      {
            \time 2/8
            g'8
            a'8
      }
    }
    '''

    assert select(staff)._get_component(scoretools.Leaf, -1) is staff[2][1]
    assert select(staff)._get_component(scoretools.Leaf, -2) is staff[2][0]
    assert select(staff)._get_component(scoretools.Leaf, -3) is staff[1][1]
    assert select(staff)._get_component(scoretools.Leaf, -4) is staff[1][0]
    assert select(staff)._get_component(scoretools.Leaf, -5) is staff[0][1]
    assert select(staff)._get_component(scoretools.Leaf, -6) is staff[0][0]


def test_selectiontools_Selection__get_component_05():

    staff = Staff(r'''
        c'16
        r16
        d'8
        r8
        e'8.
        r8.
        f'4
        r4
        ''')

    notes = [staff[0], staff[2], staff[4], staff[6]]
    rests = [staff[1], staff[3], staff[5], staff[7]]

    assert select(staff)._get_component(Note, 0) is notes[0]
    assert select(staff)._get_component(Note, 1) is notes[1]
    assert select(staff)._get_component(Note, 2) is notes[2]
    assert select(staff)._get_component(Note, 3) is notes[3]

    assert select(staff)._get_component(Rest, 0) is rests[0]
    assert select(staff)._get_component(Rest, 1) is rests[1]
    assert select(staff)._get_component(Rest, 2) is rests[2]
    assert select(staff)._get_component(Rest, 3) is rests[3]

    assert select(staff)._get_component(Staff, 0) is staff


def test_selectiontools_Selection__get_component_06():
    r'''Iterates backwards with negative values of n.
    '''

    staff = Staff(r'''
        c'16
        r16
        d'8
        r8
        e'8.
        r8.
        f'4
        r4
        ''')

    notes = [staff[0], staff[2], staff[4], staff[6]]
    rests = [staff[1], staff[3], staff[5], staff[7]]

    assert select(staff)._get_component(Note, -1) is notes[3]
    assert select(staff)._get_component(Note, -2) is notes[2]
    assert select(staff)._get_component(Note, -3) is notes[1]
    assert select(staff)._get_component(Note, -4) is notes[0]

    assert select(staff)._get_component(Rest, -1) is rests[3]
    assert select(staff)._get_component(Rest, -2) is rests[2]
    assert select(staff)._get_component(Rest, -3) is rests[1]
    assert select(staff)._get_component(Rest, -4) is rests[0]
