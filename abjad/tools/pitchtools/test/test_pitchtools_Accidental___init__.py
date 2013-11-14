# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_pitchtools_Accidental___init___01():
    r'''Accidentals can initialize from a string.
    '''
    accidental = pitchtools.Accidental('s')
    assert accidental == pitchtools.Accidental('s')


def test_pitchtools_Accidental___init___02():
    r'''Accidentals can initialize from other accidentals.
    '''
    accidental = pitchtools.Accidental(pitchtools.Accidental('s'))
    assert accidental == pitchtools.Accidental('s')


def test_pitchtools_Accidental___init___03():
    r'''Accidentals can initialize with none.
    '''
    accidental = pitchtools.Accidental(None)
    assert accidental == pitchtools.Accidental('')


def test_pitchtools_Accidental___init___04():
    r'''Accidentals can initialize with full accidental name.
    '''
    assert pitchtools.Accidental('sharp') == pitchtools.Accidental('s')
    assert pitchtools.Accidental('flat') == pitchtools.Accidental('f')
    assert pitchtools.Accidental('natural') == pitchtools.Accidental('')


def test_pitchtools_Accidental___init___05():
    assert pytest.raises(ValueError, "pitchtools.Accidental('foo')")


def test_pitchtools_Accidental___init___06():
    r'''Initializewith number.
    '''
    assert pitchtools.Accidental(0) == pitchtools.Accidental()
    assert pitchtools.Accidental(1) == pitchtools.Accidental('sharp')
    assert pitchtools.Accidental(-1) == pitchtools.Accidental('flat')
    assert pytest.raises(ValueError, "pitchtools.Accidental(99)")


def test_pitchtools_Accidental___init___07():
    r'''Initializewith symbolic string.
    '''
    assert pitchtools.Accidental('##') == pitchtools.Accidental('double sharp')
    assert pitchtools.Accidental('#') == pitchtools.Accidental('sharp')
    assert pitchtools.Accidental('b') == pitchtools.Accidental('flat')
    assert pitchtools.Accidental('bb') == pitchtools.Accidental('double flat')
