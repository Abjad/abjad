from abjad import *


def test_pitched_01( ):
   '''Rests can have pitch set with int.'''
   r = Rest((1, 4))
   r.pitch = 0
   assert isinstance(r.pitch, Pitch)
   assert repr(r) == 'Rest(4)'
   assert r.format == "c'4 \\rest"
   assert r.duration.written == r.duration.prolated == Rational(1, 4)


def test_pitched_02( ):
   '''Rests can have pitch set with Pitch.'''
   r = Rest((1, 4))
   r.pitch = Pitch(0)
   assert isinstance(r.pitch, Pitch)
   assert repr(r) == 'Rest(4)'
   assert r.format == "c'4 \\rest"
   assert r.duration.written == r.duration.prolated == Rational(1, 4)


def test_pitched_03( ):
   '''Rests can have pitch set to None.'''
   r = Rest((1, 4))
   r.pitch = None
   assert isinstance(r.pitch, type(None))
   assert repr(r) == 'Rest(4)'
   assert r.format == "r4"
   assert r.duration.written == r.duration.prolated == Rational(1, 4)
