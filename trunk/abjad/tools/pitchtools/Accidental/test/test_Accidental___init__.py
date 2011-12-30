from abjad import *
import py.test


def test_Accidental___init___01():
    '''Accidentals can initialize from a string.'''
    t = pitchtools.Accidental('s')
    assert t == pitchtools.Accidental('s')


def test_Accidental___init___02():
    '''Accidentals can initialize from other accidentals.'''
    t = pitchtools.Accidental(pitchtools.Accidental('s'))
    assert t == pitchtools.Accidental('s')


def test_Accidental___init___03():
    '''Accidentals can initialize with none.'''
    t = pitchtools.Accidental(None)
    assert t == pitchtools.Accidental('')


def test_Accidental___init___04():
    '''Accidentals can initialize with full accidental name.'''
    assert pitchtools.Accidental('sharp') == pitchtools.Accidental('s')
    assert pitchtools.Accidental('flat') == pitchtools.Accidental('f')
    assert pitchtools.Accidental('natural') == pitchtools.Accidental('')


def test_Accidental___init___05():
    assert py.test.raises(ValueError, "pitchtools.Accidental('foo')")


def test_Accidental___init___06():
    '''Init with number.'''
    assert pitchtools.Accidental(0) == pitchtools.Accidental()
    assert pitchtools.Accidental(1) == pitchtools.Accidental('sharp')
    assert pitchtools.Accidental(-1) == pitchtools.Accidental('flat')
    assert py.test.raises(ValueError, "pitchtools.Accidental(99)")


def test_Accidental___init___07():
    '''Init with symbolic string.'''
    assert pitchtools.Accidental('##') == pitchtools.Accidental('double sharp')
    assert pitchtools.Accidental('#') == pitchtools.Accidental('sharp')
    assert pitchtools.Accidental('b') == pitchtools.Accidental('flat')
    assert pitchtools.Accidental('bb') == pitchtools.Accidental('double flat')
