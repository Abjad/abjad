# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_marktools_Articulation_01():
    r'''Articulations can be initialized from zero, one or two arguments.
    '''

    a = marktools.Articulation()
    assert a.name == None
    assert a.direction is None
    a = marktools.Articulation('^\\marcato')
    assert a.name == 'marcato'
    assert a.direction is Up
    a = marktools.Articulation('legato', Down)
    assert a.name == 'legato'
    assert a.direction is Down


def test_marktools_Articulation_02():
    r'''Articulations have string and direction.
    '''

    note = Note("c'4")
    a = marktools.Articulation('staccato')(note)
    assert a.name == 'staccato'
    assert a.direction is None


def test_marktools_Articulation_03():
    r'''Articulation name can be set to none.
    '''

    note = Note("c'4")
    a = marktools.Articulation()(note)
    assert a.name is None
    assert str(a) == ''


def test_marktools_Articulation_04():
    r'''Direction can be set to None.
    '''

    note = Note("c'4")
    a = marktools.Articulation('staccato', None)(note)
    assert a.direction is None
    assert str(a) == r'-\staccato'


def test_marktools_Articulation_05():
    r'''Direction can be set to up.
    '''

    note = Note("c'4")
    a = marktools.Articulation('staccato', Up)(note)
    assert a.direction is Up
    assert str(a) == r'^\staccato'

    a = marktools.Articulation('staccato', '^')
    assert a.direction is Up
    assert str(a) == r'^\staccato'


def test_marktools_Articulation_06():
    r'''Direction can be set to down.
    '''

    note = Note("c'4")
    a = marktools.Articulation('staccato', Down)(note)
    assert a.direction is Down
    assert str(a) == r'_\staccato'

    a = marktools.Articulation('staccato', '_')
    assert a.direction is Down
    assert str(a) == r'_\staccato'


def test_marktools_Articulation_07():
    r'''Direction can be set to default.
    '''

    note = Note("c'4")
    a = marktools.Articulation('staccato')
    assert a.direction is None
    assert str(a) == r'-\staccato'

    a = marktools.Articulation('staccato', '-')
    assert a.direction is Center
    assert str(a) == r'-\staccato'



def test_marktools_Articulation_08():
    r'''Shortcut strings are replaced with full word.
    '''

    note = Note("c'4")
    a = marktools.Articulation('.')(note)
    assert a.name == '.'
    assert str(a) == r'-\staccato'

    a = marktools.Articulation('-')
    assert a.name == '-'
    assert str(a) == r'-\tenuto'

    a = marktools.Articulation('|')
    assert a.name == '|'
    assert str(a) == r'-\staccatissimo'
