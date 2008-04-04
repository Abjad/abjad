from abjad import *


def test_scopy_01( ):
   '''Container.'''
   t = Container(Note(0, (1, 8)) * 3)
   new = scopy(t, 0, (3, 16))
   assert isinstance(new, Container)
   assert len(new) == 2
   assert new.duration == (3, 16)
   assert new[0].duration == (1, 8)
   assert new[1].duration == (1, 16)
   assert check(new)


def test_scopy_01b( ):
   '''Container with rest.'''
   t = Container([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
   new = scopy(t, 0, (3, 16))
   assert isinstance(new, Container)
   assert len(new) == 2
   assert new.duration == (3, 16)
   assert isinstance(new[0], Note)
   assert isinstance(new[1], Rest)
   assert new[0].duration == (1, 8)
   assert new[1].duration == (1, 16)
   assert check(new)


def test_scopy_02( ):
   '''Measure.'''
   t = Measure((3, 8), Note(0, (1, 8)) * 3)
   new = scopy(t, 0, (3, 16))
   assert isinstance(new, Measure)
   assert new.meter == (3, 16)
   assert len(new) == 2
   assert new.duration == (3, 16)
   assert new[0].duration == (1, 8)
   assert new[1].duration == (1, 16)
   assert check(new)


def test_scopy_03( ):
   '''Fixed duration tuplet.'''
   t = FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)
   new = scopy(t, 0, (1, 8))
   assert isinstance(new, FixedDurationTuplet)
   assert len(new) == 2
   assert new.duration == Rational(1, 8) 
   assert new[0].duration == Rational(1, 8)
   assert new[0].duration.prolated == Rational(1, 12)
   assert new[1].duration == Rational(1, 16)
   assert new[1].duration.prolated == Rational(1, 24)
   assert check(new)


def test_scopy_04( ):
   '''Fixed multiplier tuplet.'''
   t = FixedMultiplierTuplet((2, 3), Note(0, (1, 8)) * 3)
   new = scopy(t, 0, (1, 8))
   assert isinstance(new, FixedMultiplierTuplet)
   assert len(new) == 2
   assert new.duration == Rational(1, 8) 
   assert new[0].duration == Rational(1, 8)
   assert new[0].duration.prolated == Rational(1, 12)
   assert new[1].duration == Rational(1, 16)
   assert new[1].duration.prolated == Rational(1, 24)
   assert check(new)


def test_scopy_05( ):
   '''Voice.'''
   t = Voice(Note(0, (1, 8)) * 3)
   new = scopy(t, 0, (3, 16))
   assert isinstance(new, Voice)
   assert len(new) == 2
   assert new.duration == (3, 16)
   assert new[0].duration == (1, 8)
   assert new[1].duration == (1, 16)
   assert check(new)


def test_scopy_06( ):
   '''Staff.'''
   t = Staff(Note(0, (1, 8)) * 3)
   new = scopy(t, 0, (3, 16))
   assert isinstance(new, Staff)
   assert len(new) == 2
   assert new.duration == (3, 16)
   assert new[0].duration == (1, 8)
   assert new[1].duration == (1, 16)
   assert check(new)
