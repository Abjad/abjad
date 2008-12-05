from abjad import *
from py.test import raises


def test_harmonic_interface_01( ):
   '''Add a natural harmonic.'''
   t = Note(0, (1, 4))
   t.harmonic = True
   assert t.format == "c'4 \\flageolet"


def test_harmonic_interface_02( ):
   '''Add and then clear a natural harmonic with False.'''
   t = Note(0, (1, 4))
   t.harmonic = True
   t.harmonic = False
   assert t.format == "c'4"


def test_harmonic_interface_03( ):
   '''Add and then clear a natural harmonic with None.'''
   t = Note(0, (1, 4))
   t.harmonic = True
   t.harmonic = None
   assert t.format == "c'4"


def test_harmonic_interface_04( ):
   '''Values other than True, False and None raise an exception.'''
   t = Note(0, (1, 4))
   assert raises(ValueError, "t.harmonic = 'foo'")
