from abjad import *
import py.test


def test_Articulation_01():
    '''Articulations can be initialized from zero, one or two arguments.
    '''

    a = marktools.Articulation()
    assert a.name == None
    assert a.direction_string is None
    a = marktools.Articulation('^\\marcato')
    assert a.name == 'marcato'
    assert a.direction_string == '^'
    a = marktools.Articulation('legato', 'down')
    assert a.name == 'legato'
    assert a.direction_string == '_'


def test_Articulation_02():
    '''Articulations have string and direction.
    '''

    t = Note("c'4")
    a = marktools.Articulation('staccato')(t)
    assert a.name == 'staccato'
    assert a.direction_string is None


def test_Articulation_03():
    '''Articulation name can be set to none.
    '''

    t = Note("c'4")
    a = marktools.Articulation()(t)
    assert a.name is None
    assert str(a) == ''


def test_Articulation_04():
    '''Direction can be set to None.
    '''

    t = Note("c'4")
    a = marktools.Articulation('staccato', None)(t)
    assert a.direction_string is None
    assert str(a) == r'-\staccato'


def test_Articulation_05():
    '''Direction can be set to up.
    '''

    t = Note("c'4")
    a = marktools.Articulation('staccato', 'up')(t)
    assert a.direction_string == '^'
    assert str(a) == r'^\staccato'

    a = marktools.Articulation('staccato', '^')
    assert a.direction_string == '^'
    assert str(a) == r'^\staccato'


def test_Articulation_06():
    '''Direction can be set to down.
    '''

    t = Note("c'4")
    a = marktools.Articulation('staccato', 'down')(t)
    assert a.direction_string == '_'
    assert str(a) == r'_\staccato'

    a = marktools.Articulation('staccato', '_')
    assert a.direction_string == '_'
    assert str(a) == r'_\staccato'


def test_Articulation_07():
    '''Direction can be set to default.
    '''

    t = Note("c'4")
    a = marktools.Articulation('staccato')
    assert a.direction_string is None
    assert str(a) == r'-\staccato'

    a = marktools.Articulation('staccato', '-')
    assert a.direction_string == '-'
    assert str(a) == r'-\staccato'



def test_Articulation_08():
    '''Shortcut strings are replaced with full word.
    '''

    t = Note("c'4")
    a = marktools.Articulation('.')(t)
    assert a.name == '.'
    assert str(a) == r'-\staccato'

    a = marktools.Articulation('-')
    assert a.name == '-'
    assert str(a) == r'-\tenuto'

    a = marktools.Articulation('|')
    assert a.name == '|'
    assert str(a) == r'-\staccatissimo'
