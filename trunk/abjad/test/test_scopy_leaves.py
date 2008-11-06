from abjad import *


### Anatomy of the tests:
###   there are five different timepoints relative to the timespan of a note:
###     1. 'before', ie a negative number
###     2. 'start', ie 0 which is the startpoint of the timespan
###     3. 'mid', ie some value y such that 0 < y < t.duration.prolated
###     4. 'stop', ie t.duration.prolated
###     5. 'after', ie some value z such that t.duration.prolated < z


def test_scopy_leaves_01( ):
   '''Start-to-mid clean cut.'''
   t = Note(0, (1, 4))
   new = scopy(t, 0, (1, 8))
   assert isinstance(new, Note)
   assert t.pitch.number == new.pitch.number
   #assert new.duration == Rational(1, 8)
   assert new.duration.written == Rational(1, 8)


def test_scopy_leaves_02( ):
   '''Start-to-mid jagged cut.'''
   t = Note(0, (1, 4))
   new = scopy(t, 0, (1, 12))
   assert isinstance(new, FixedDurationTuplet)
   #assert new.duration == Rational(1, 12)
   assert new.duration.target == Rational(1, 12)
   assert len(new) == 1
   #assert new[0].duration == Rational(1, 8)
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[0].duration.prolated == Rational(1, 12)
  

def test_scopy_leaves_03( ):
   '''Mid-mid jagged cut.'''
   t = Note(0, (1, 4))
   new = scopy(t, (1, 12), (2, 12)) 
   assert isinstance(new, FixedDurationTuplet)
   #assert new.duration == Rational(1, 12)
   assert new.duration.target == Rational(1, 12)
   assert len(new) == 1
   #assert new[0].duration == Rational(1, 8)
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[0].duration.prolated == Rational(1, 12)


def test_scopy_leaves_04( ):
   '''Mid-to-stop jagged cut.'''
   t = Note(0, (1, 4))
   new = scopy(t, (1, 6), (1, 4))
   assert isinstance(new, FixedDurationTuplet)
   #assert new.duration == Rational(1, 12)
   assert new.duration.target == Rational(1, 12)
   assert len(new) == 1
   #assert new[0].duration == Rational(1, 8)
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[0].duration.prolated == Rational(1, 12)
  

def test_scopy_leaves_05( ):
   '''Start-to-after clean cut.'''
   t = Note(0, (1, 4))
   new = scopy(t, 0, (1, 2))
   assert isinstance(new, Note)
   #assert new.duration == Rational(1, 4)
   assert new.duration.written == Rational(1, 4)


def test_scopy_leaves_06( ):
   '''Mid-to-after clean cut.'''
   t = Note(0, (1, 4))
   new = scopy(t, (1, 8), (1, 2))
   assert isinstance(new, Note)
   #assert new.duration == Rational(1, 8)
   assert new.duration.written == Rational(1, 8)


def test_scopy_leaves_07( ):
   '''Mid-to-after jagged cut.'''
   t = Note(0, (1, 4))
   new = scopy(t, (2, 12), (1, 2))
   assert isinstance(new, FixedDurationTuplet)
   #assert new.duration == Rational(1, 12)
   assert new.duration.target == Rational(1, 12)
   #assert new[0].duration == Rational(1, 8)
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[0].duration.prolated == Rational(1, 12)


def test_scopy_leaves_08( ):
   '''Before-to-after.'''
   t = Note(0, (1, 4))
   new = scopy(t, (-1, 4), (1, 2))
   assert isinstance(new, Note)
   #assert new.duration == Rational(1, 4)
   assert new.duration.written == Rational(1, 4)


def test_scopy_leaves_09( ):
   '''Start-to-mid jagged.'''
   t = Note(0, (1, 4))
   new = scopy(t, 0, (5, 24))
   assert isinstance(new, FixedDurationTuplet)
   #assert new.duration == Rational(5, 24)
   assert new.duration.target == Rational(5, 24)
   assert len(new) == 1
   #assert new[0].duration == Rational(1, 4)
   assert new[0].duration.preprolated == Rational(1, 4)
   assert new[0].duration.prolated == Rational(5, 24)


def test_scopy_leaves_10( ):
   '''Start-to-mid jagged. '''
   t = Note(0, (1, 4))
   new = scopy(t, 0, (1, 5))
   assert isinstance(new, FixedDurationTuplet)
   assert len(new) == 1
   #assert new.duration == Rational(1, 5)
   assert new.duration.target == Rational(1, 5)
   #assert new[0].duration == Rational(1, 4)
   assert new[0].duration.preprolated == Rational(1, 4)
   assert new[0].duration.prolated == Rational(1, 5)
