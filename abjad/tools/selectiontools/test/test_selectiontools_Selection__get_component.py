# -*- coding: utf-8 -*-
import abjad


def test_selectiontools_Selection__get_component_01():

    staff = abjad.Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    assert abjad.select(staff)._get_component(abjad.Measure, 0) is staff[0]
    assert abjad.select(staff)._get_component(abjad.Measure, 1) is staff[1]
    assert abjad.select(staff)._get_component(abjad.Measure, 2) is staff[2]


def test_selectiontools_Selection__get_component_02():

    staff = abjad.Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    assert abjad.select(staff)._get_component(abjad.Measure, -1) is staff[2]
    assert abjad.select(staff)._get_component(abjad.Measure, -2) is staff[1]
    assert abjad.select(staff)._get_component(abjad.Measure, -3) is staff[0]


def test_selectiontools_Selection__get_component_03():
    r'''Read forwards for positive n.
    '''

    staff = abjad.Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

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

    assert abjad.select(staff)._get_component(abjad.Leaf, 0) is staff[0][0]
    assert abjad.select(staff)._get_component(abjad.Leaf, 1) is staff[0][1]
    assert abjad.select(staff)._get_component(abjad.Leaf, 2) is staff[1][0]
    assert abjad.select(staff)._get_component(abjad.Leaf, 3) is staff[1][1]
    assert abjad.select(staff)._get_component(abjad.Leaf, 4) is staff[2][0]
    assert abjad.select(staff)._get_component(abjad.Leaf, 5) is staff[2][1]


def test_selectiontools_Selection__get_component_04():
    r'''Read backwards for negative n.
    '''

    staff = abjad.Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

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

    assert abjad.select(staff)._get_component(abjad.Leaf, -1) is staff[2][1]
    assert abjad.select(staff)._get_component(abjad.Leaf, -2) is staff[2][0]
    assert abjad.select(staff)._get_component(abjad.Leaf, -3) is staff[1][1]
    assert abjad.select(staff)._get_component(abjad.Leaf, -4) is staff[1][0]
    assert abjad.select(staff)._get_component(abjad.Leaf, -5) is staff[0][1]
    assert abjad.select(staff)._get_component(abjad.Leaf, -6) is staff[0][0]


def test_selectiontools_Selection__get_component_05():

    staff = abjad.Staff(r'''
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

    assert abjad.select(staff)._get_component(abjad.Note, 0) is notes[0]
    assert abjad.select(staff)._get_component(abjad.Note, 1) is notes[1]
    assert abjad.select(staff)._get_component(abjad.Note, 2) is notes[2]
    assert abjad.select(staff)._get_component(abjad.Note, 3) is notes[3]

    assert abjad.select(staff)._get_component(abjad.Rest, 0) is rests[0]
    assert abjad.select(staff)._get_component(abjad.Rest, 1) is rests[1]
    assert abjad.select(staff)._get_component(abjad.Rest, 2) is rests[2]
    assert abjad.select(staff)._get_component(abjad.Rest, 3) is rests[3]

    assert abjad.select(staff)._get_component(abjad.Staff, 0) is staff


def test_selectiontools_Selection__get_component_06():
    r'''Iterates backwards with negative values of n.
    '''

    staff = abjad.Staff(r'''
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

    assert abjad.select(staff)._get_component(abjad.Note, -1) is notes[3]
    assert abjad.select(staff)._get_component(abjad.Note, -2) is notes[2]
    assert abjad.select(staff)._get_component(abjad.Note, -3) is notes[1]
    assert abjad.select(staff)._get_component(abjad.Note, -4) is notes[0]

    assert abjad.select(staff)._get_component(abjad.Rest, -1) is rests[3]
    assert abjad.select(staff)._get_component(abjad.Rest, -2) is rests[2]
    assert abjad.select(staff)._get_component(abjad.Rest, -3) is rests[1]
    assert abjad.select(staff)._get_component(abjad.Rest, -4) is rests[0]
