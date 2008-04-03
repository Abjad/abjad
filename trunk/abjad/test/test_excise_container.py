from abjad import *


def test_excise_container_01( ):
   '''Plain vanilla container.'''
   t = Container(Note(0, (1, 4)) * 6)
   excise(t.leaves[0])
   assert isinstance(t, Container)
   assert len(t) == 5
   assert t.duration == Rational(5, 4)
   assert t.duration.prolated == Rational(5, 4)
   assert isinstance(t[0], Note)
   assert t[0].duration == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 4)
   assert check(t)


def test_excise_container_02( ):
   '''Sequential container.'''
   t = Sequential(Note(0, (1, 4)) * 6)
   excise(t.leaves[0])
   assert isinstance(t, Sequential)
   assert len(t) == 5
   assert t.duration == Rational(5, 4)
   assert t.duration.prolated == Rational(5, 4)
   assert isinstance(t[0], Note)
   assert t[0].duration == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 4)
   assert check(t)


def test_excise_container_03( ):
   '''Voice.'''
   t = Voice(Note(0, (1, 4)) * 6)
   excise(t.leaves[0])
   assert isinstance(t, Voice)
   assert len(t) == 5
   assert t.duration == Rational(5, 4)
   assert t.duration.prolated == Rational(5, 4)
   assert isinstance(t[0], Note)
   assert t[0].duration == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 4)
   assert check(t)


def test_excise_container_04( ):
   '''Staff.'''
   t = Staff(Note(0, (1, 4)) * 6)
   excise(t.leaves[0])
   assert isinstance(t, Staff)
   assert len(t) == 5
   assert t.duration == Rational(5, 4)
   assert t.duration.prolated == Rational(5, 4)
   assert isinstance(t[0], Note)
   assert t[0].duration == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 4)
   assert check(t)


def test_excise_container_05( ):
   '''Container.'''
   t = Container(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   excise(t[0])
   assert isinstance(t, Container)
   assert len(t) == 1
   assert t.duration == Rational(2, 4)
   assert t.duration.prolated == Rational(2, 4)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration == Rational(2, 4)
   assert t[0].duration.prolated == Rational(2, 4)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check(t)


def test_excise_container_06( ):
   '''Sequential.'''
   t = Sequential(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   excise(t[0])
   assert isinstance(t, Sequential)
   assert len(t) == 1
   assert t.duration == Rational(2, 4)
   assert t.duration.prolated == Rational(2, 4)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration == Rational(2, 4)
   assert t[0].duration.prolated == Rational(2, 4)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check(t)


def test_excise_container_07( ):
   '''Voice.'''
   t = Voice(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   excise(t[0])
   assert isinstance(t, Voice)
   assert len(t) == 1
   assert t.duration == Rational(2, 4)
   assert t.duration.prolated == Rational(2, 4)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration == Rational(2, 4)
   assert t[0].duration.prolated == Rational(2, 4)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check(t)


def test_excise_container_08( ):
   '''Staff.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   excise(t[0])
   assert isinstance(t, Staff)
   assert len(t) == 1
   assert t.duration == Rational(2, 4)
   assert t.duration.prolated == Rational(2, 4)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration == Rational(2, 4)
   assert t[0].duration.prolated == Rational(2, 4)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check(t)


def test_excise_container_09( ):
   '''Container.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   excise(t.leaves[0])
   assert isinstance(t, Staff)
   assert len(t) == 2
   assert t.duration == Rational(5, 6)
   assert t.duration.prolated == Rational(5, 6)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration == Rational(2, 6)
   assert t[0].duration.prolated == Rational(2, 6)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check(t)


def test_excise_container_10( ):
   '''Sequential.'''
   t = Sequential(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   excise(t.leaves[0])
   assert isinstance(t, Sequential)
   assert len(t) == 2
   assert t.duration == Rational(5, 6)
   assert t.duration.prolated == Rational(5, 6)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration == Rational(2, 6)
   assert t[0].duration.prolated == Rational(2, 6)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check(t)


def test_excise_container_11( ):
   '''Voice.'''
   t = Voice(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   excise(t.leaves[0])
   assert isinstance(t, Voice)
   assert len(t) == 2
   assert t.duration == Rational(5, 6)
   assert t.duration.prolated == Rational(5, 6)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration == Rational(2, 6)
   assert t[0].duration.prolated == Rational(2, 6)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check(t)


def test_excise_container_12( ):
   '''Staff.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   excise(t.leaves[0])
   assert isinstance(t, Staff)
   assert len(t) == 2
   assert t.duration == Rational(5, 6)
   assert t.duration.prolated == Rational(5, 6)
   assert isinstance(t[0], FixedDurationTuplet)
   assert t[0].duration == Rational(2, 6)
   assert t[0].duration.prolated == Rational(2, 6)
   assert isinstance(t[0][0], Note)
   assert t[0][0].duration == Rational(1, 4)
   assert t[0][0].duration.prolated == Rational(1, 6)
   assert check(t)
