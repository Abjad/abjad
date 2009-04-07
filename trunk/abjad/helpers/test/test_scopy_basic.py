from abjad import *


def test_scopy_basic_01( ):
   '''Container.'''
   t = Container(Note(0, (1, 8)) * 3)
   new = scopy(t, 0, (3, 16))
   assert isinstance(new, Container)
   assert len(new) == 2
   assert new.duration.contents == Rational(3, 16)
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[1].duration.preprolated == Rational(1, 16)
   assert check(new)


def test_scopy_basic_01b( ):
   '''Container with rest.'''
   t = Container([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
   new = scopy(t, 0, (3, 16))
   assert isinstance(new, Container)
   assert len(new) == 2
   assert new.duration.contents == Rational(3, 16)
   assert isinstance(new[0], Note)
   assert isinstance(new[1], Rest)
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[1].duration.preprolated == Rational(1, 16)
   assert check(new)


def test_scopy_basic_02( ):
   '''RigidMeasure.'''
   t = RigidMeasure((3, 8), Note(0, (1, 8)) * 3)
   new = scopy(t, 0, (3, 16))
   assert isinstance(new, RigidMeasure)
   assert new.meter.forced == (3, 16)
   assert len(new) == 2
   assert new.duration.contents == Rational(3, 16)
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[1].duration.preprolated == Rational(1, 16)
   assert check(new)


def test_scopy_basic_03( ):
   '''Fixed duration tuplet.'''
   t = FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)
   new = scopy(t, 0, (1, 8))
   assert isinstance(new, FixedDurationTuplet)
   assert len(new) == 2
   assert new.duration.target == Rational(1, 8) 
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[0].duration.prolated == Rational(1, 12)
   assert new[1].duration.preprolated == Rational(1, 16)
   assert new[1].duration.prolated == Rational(1, 24)
   assert check(new)


def test_scopy_basic_04( ):
   '''Fixed multiplier tuplet.'''
   t = FixedMultiplierTuplet((2, 3), Note(0, (1, 8)) * 3)
   new = scopy(t, 0, (1, 8))
   assert isinstance(new, FixedMultiplierTuplet)
   assert len(new) == 2
   assert new.duration.preprolated == Rational(1, 8) 
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[0].duration.prolated == Rational(1, 12)
   assert new[1].duration.preprolated == Rational(1, 16)
   assert new[1].duration.prolated == Rational(1, 24)
   assert check(new)


def test_scopy_basic_05( ):
   '''Voice.'''
   t = Voice(Note(0, (1, 8)) * 3)
   new = scopy(t, 0, (3, 16))
   assert isinstance(new, Voice)
   assert len(new) == 2
   assert new.duration.contents == Rational(3, 16)
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[1].duration.preprolated == Rational(1, 16)
   assert check(new)


def test_scopy_basic_06( ):
   '''Staff.'''
   t = Staff(Note(0, (1, 8)) * 3)
   new = scopy(t, 0, (3, 16))
   assert isinstance(new, Staff)
   assert len(new) == 2
   assert new.duration.contents == Rational(3, 16)
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[1].duration.preprolated == Rational(1, 16)
   assert check(new)
