# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_Articulation___init___01():
    r'''Articulations can be initialized from zero, one or two arguments.
    '''

    articulation = Articulation('^\\marcato')
    assert articulation.name == 'marcato'
    assert articulation.direction == Up
    articulation = Articulation('legato', Down)
    assert articulation.name == 'legato'
    assert articulation.direction == Down


def test_indicatortools_Articulation___init___02():
    r'''Articulations have string and direction.
    '''

    note = Note("c'4")
    articulation = Articulation('staccato')
    attach(articulation, note)
    assert articulation.name == 'staccato'
    assert articulation.direction is None


def test_indicatortools_Articulation___init___03():
    r'''Direction can be set to None.
    '''

    note = Note("c'4")
    articulation = Articulation('staccato', None)
    attach(articulation, note)
    assert articulation.direction is None
    assert str(articulation) == r'-\staccato'


def test_indicatortools_Articulation___init___04():
    r'''Direction can be set to up.
    '''

    note = Note("c'4")
    articulation = Articulation('staccato', Up)
    attach(articulation, note)
    assert articulation.direction == Up
    assert str(articulation) == r'^\staccato'

    articulation = Articulation('staccato', '^')
    assert articulation.direction == Up
    assert str(articulation) == r'^\staccato'


def test_indicatortools_Articulation___init___05():
    r'''Direction can be set to down.
    '''

    note = Note("c'4")
    articulation = Articulation('staccato', Down)
    attach(articulation, note)
    assert articulation.direction == Down
    assert str(articulation) == r'_\staccato'

    articulation = Articulation('staccato', '_')
    assert articulation.direction == Down
    assert str(articulation) == r'_\staccato'


def test_indicatortools_Articulation___init___06():
    r'''Direction can be set to default.
    '''

    note = Note("c'4")
    articulation = Articulation('staccato')
    assert articulation.direction is None
    assert str(articulation) == r'-\staccato'

    articulation = Articulation('staccato', '-')
    assert articulation.direction == Center
    assert str(articulation) == r'-\staccato'



def test_indicatortools_Articulation___init___07():
    r'''Shortcut strings are replaced with full word.
    '''

    note = Note("c'4")
    articulation = Articulation('.')
    attach(articulation, note)
    assert articulation.name == '.'
    assert str(articulation) == r'-\staccato'

    articulation = Articulation('-')
    assert articulation.name == '-'
    assert str(articulation) == r'-\tenuto'

    articulation = Articulation('|')
    assert articulation.name == '|'
    assert str(articulation) == r'-\staccatissimo'
