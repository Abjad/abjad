# -*- encoding: utf-8 -*-
import py.test
from abjad import *


def test_marktools_Articulation_01():
    r'''Articulations can be initialized from zero, one or two arguments.
    '''

    articulation = marktools.Articulation()
    assert articulation.name == None
    assert articulation.direction is None
    articulation = marktools.Articulation('^\\marcato')
    assert articulation.name == 'marcato'
    assert articulation.direction is Up
    articulation = marktools.Articulation('legato', Down)
    assert articulation.name == 'legato'
    assert articulation.direction is Down


def test_marktools_Articulation_02():
    r'''Articulations have string and direction.
    '''

    note = Note("c'4")
    articulation = marktools.Articulation('staccato')
    articulation.attach(note)
    assert articulation.name == 'staccato'
    assert articulation.direction is None


def test_marktools_Articulation_03():
    r'''Articulation name can be set to none.
    '''

    note = Note("c'4")
    articulation = marktools.Articulation()
    articulation.attach(note)
    assert articulation.name is None
    assert str(articulation) == ''


def test_marktools_Articulation_04():
    r'''Direction can be set to None.
    '''

    note = Note("c'4")
    articulation = marktools.Articulation('staccato', None)
    articulation.attach(note)
    assert articulation.direction is None
    assert str(articulation) == r'-\staccato'


def test_marktools_Articulation_05():
    r'''Direction can be set to up.
    '''

    note = Note("c'4")
    articulation = marktools.Articulation('staccato', Up)
    articulation.attach(note)
    assert articulation.direction is Up
    assert str(articulation) == r'^\staccato'

    articulation = marktools.Articulation('staccato', '^')
    assert articulation.direction is Up
    assert str(articulation) == r'^\staccato'


def test_marktools_Articulation_06():
    r'''Direction can be set to down.
    '''

    note = Note("c'4")
    articulation = marktools.Articulation('staccato', Down)
    articulation.attach(note)
    assert articulation.direction is Down
    assert str(articulation) == r'_\staccato'

    articulation = marktools.Articulation('staccato', '_')
    assert articulation.direction is Down
    assert str(articulation) == r'_\staccato'


def test_marktools_Articulation_07():
    r'''Direction can be set to default.
    '''

    note = Note("c'4")
    articulation = marktools.Articulation('staccato')
    assert articulation.direction is None
    assert str(articulation) == r'-\staccato'

    articulation = marktools.Articulation('staccato', '-')
    assert articulation.direction is Center
    assert str(articulation) == r'-\staccato'



def test_marktools_Articulation_08():
    r'''Shortcut strings are replaced with full word.
    '''

    note = Note("c'4")
    articulation = marktools.Articulation('.')
    articulation.attach(note)
    assert articulation.name == '.'
    assert str(articulation) == r'-\staccato'

    articulation = marktools.Articulation('-')
    assert articulation.name == '-'
    assert str(articulation) == r'-\tenuto'

    articulation = marktools.Articulation('|')
    assert articulation.name == '|'
    assert str(articulation) == r'-\staccatissimo'
