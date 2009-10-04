from abjad import *
from abjad.tuplet.tuplet import _Tuplet


def test_clonewp_by_duration_with_parentage_01( ):
   '''Container.'''
   t = Container(Note(0, (1, 8)) * 3)
   new = clonewp.by_duration_with_parentage(t, 0, (3, 16))
   assert isinstance(new, Container)
   assert len(new) == 2
   assert new.duration.contents == Rational(3, 16)
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[1].duration.preprolated == Rational(1, 16)
   assert check.wf(new)


def test_clonewp_by_duration_with_parentage01b( ):
   '''Container with rest.'''
   t = Container([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
   new = clonewp.by_duration_with_parentage(t, 0, (3, 16))
   assert isinstance(new, Container)
   assert len(new) == 2
   assert new.duration.contents == Rational(3, 16)
   assert isinstance(new[0], Note)
   assert isinstance(new[1], Rest)
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[1].duration.preprolated == Rational(1, 16)
   assert check.wf(new)


def test_clonewp_by_duration_with_parentage_02( ):
   '''RigidMeasure.'''
   t = RigidMeasure((3, 8), Note(0, (1, 8)) * 3)
   new = clonewp.by_duration_with_parentage(t, 0, (3, 16))
   assert isinstance(new, RigidMeasure)
   assert new.meter.forced == (3, 16)
   assert len(new) == 2
   assert new.duration.contents == Rational(3, 16)
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[1].duration.preprolated == Rational(1, 16)
   assert check.wf(new)


def test_clonewp_by_duration_with_parentage_03( ):
   '''Fixed duration tuplet.'''
   t = FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)
   new = clonewp.by_duration_with_parentage(t, 0, (1, 8))
   assert isinstance(new, FixedDurationTuplet)
   assert len(new) == 2
   assert new.duration.target == Rational(1, 8) 
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[0].duration.prolated == Rational(1, 12)
   assert new[1].duration.preprolated == Rational(1, 16)
   assert new[1].duration.prolated == Rational(1, 24)
   assert check.wf(new)


def test_clonewp_by_duration_with_parentage_04( ):
   '''Fixed multiplier tuplet.'''
   t = FixedMultiplierTuplet((2, 3), Note(0, (1, 8)) * 3)
   new = clonewp.by_duration_with_parentage(t, 0, (1, 8))
   assert isinstance(new, FixedMultiplierTuplet)
   assert len(new) == 2
   assert new.duration.preprolated == Rational(1, 8) 
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[0].duration.prolated == Rational(1, 12)
   assert new[1].duration.preprolated == Rational(1, 16)
   assert new[1].duration.prolated == Rational(1, 24)
   assert check.wf(new)


def test_clonewp_by_duration_with_parentage_05( ):
   '''Voice.'''
   t = Voice(Note(0, (1, 8)) * 3)
   new = clonewp.by_duration_with_parentage(t, 0, (3, 16))
   assert isinstance(new, Voice)
   assert len(new) == 2
   assert new.duration.contents == Rational(3, 16)
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[1].duration.preprolated == Rational(1, 16)
   assert check.wf(new)


def test_clonewp_by_duration_with_parentage_06( ):
   '''Staff.'''
   t = Staff(Note(0, (1, 8)) * 3)
   new = clonewp.by_duration_with_parentage(t, 0, (3, 16))
   assert isinstance(new, Staff)
   assert len(new) == 2
   assert new.duration.contents == Rational(3, 16)
   assert new[0].duration.preprolated == Rational(1, 8)
   assert new[1].duration.preprolated == Rational(1, 16)
   assert check.wf(new)


## Anatomy of the tests:
##   there are five different timepoints relative to the timespan of a note:
##     1. 'before', ie a negative number
##     2. 'start', ie 0 which is the startpoint of the timespan
##     3. 'mid', ie some value y such that 0 < y < t.duration.prolated
##     4. 'stop', ie t.duration.prolated
##     5. 'after', ie some value z such that t.duration.prolated < z


def test_clonewp_by_duration_with_parentage_01( ):
   '''Start-to-mid clean cut.'''
   t = Note(0, (1, 4))
   new = clonewp.by_duration_with_parentage(t, 0, (1, 8))
   assert isinstance(new, Note)
   assert t.pitch.number == new.pitch.number
   assert new.duration.written == Rational(1, 8)


def test_clonewp_by_duration_with_parentage_02( ):
   '''Start-to-mid jagged cut.'''
   t = Note(0, (1, 4))
   new = clonewp.by_duration_with_parentage(t, 0, (1, 12))
   assert isinstance(new, Note)
   assert isinstance(new.parentage.parent, _Tuplet)
   assert new.duration.preprolated == Rational(1, 8)
   assert new.duration.prolated == Rational(1, 12)
  

def test_clonewp_by_duration_with_parentage_03( ):
   '''Mid-mid jagged cut.'''
   t = Note(0, (1, 4))
   new = clonewp.by_duration_with_parentage(t, (1, 12), (2, 12)) 
   assert isinstance(new, Note)
   assert isinstance(new.parentage.parent, _Tuplet)
   assert new.duration.preprolated == Rational(1, 8)
   assert new.duration.prolated == Rational(1, 12)


def test_clonewp_by_duration_with_parentage_04( ):
   '''Mid-to-stop jagged cut.'''
   t = Note(0, (1, 4))
   new = clonewp.by_duration_with_parentage(t, (1, 6), (1, 4))
#   assert isinstance(new, FixedDurationTuplet)
#   assert new.duration.target == Rational(1, 12)
#   assert len(new) == 1
#   assert new[0].duration.preprolated == Rational(1, 8)
#   assert new[0].duration.prolated == Rational(1, 12)
   assert isinstance(new, Note)
   assert isinstance(new.parentage.parent, _Tuplet)
   assert new.duration.preprolated == Rational(1, 8)
   assert new.duration.prolated == Rational(1, 12)
  

def test_clonewp_by_duration_with_parentage_05( ):
   '''Start-to-after clean cut.'''
   t = Note(0, (1, 4))
   new = clonewp.by_duration_with_parentage(t, 0, (1, 2))
   assert isinstance(new, Note)
   assert new.duration.written == Rational(1, 4)


def test_clonewp_by_duration_with_parentage_06( ):
   '''Mid-to-after clean cut.'''
   t = Note(0, (1, 4))
   new = clonewp.by_duration_with_parentage(t, (1, 8), (1, 2))
   assert isinstance(new, Note)
   assert new.duration.written == Rational(1, 8)


def test_clonewp_by_duration_with_parentage_07( ):
   '''Mid-to-after jagged cut.'''
   t = Note(0, (1, 4))
   new = clonewp.by_duration_with_parentage(t, (2, 12), (1, 2))
#   assert isinstance(new, FixedDurationTuplet)
#   assert new.duration.target == Rational(1, 12)
#   assert new[0].duration.preprolated == Rational(1, 8)
#   assert new[0].duration.prolated == Rational(1, 12)
   assert isinstance(new, Note)
   assert isinstance(new.parentage.parent, _Tuplet)
   assert new.duration.preprolated == Rational(1, 8)
   assert new.duration.prolated == Rational(1, 12)


def test_clonewp_by_duration_with_parentage_08( ):
   '''Before-to-after.'''
   t = Note(0, (1, 4))
   new = clonewp.by_duration_with_parentage(t, (-1, 4), (1, 2))
   assert isinstance(new, Note)
   assert new.duration.written == Rational(1, 4)


def test_clonewp_by_duration_with_parentage_09( ):
   '''Start-to-mid jagged.'''
   t = Note(0, (1, 4))
   new = clonewp.by_duration_with_parentage(t, 0, (5, 24))
   #assert isinstance(new, FixedDurationTuplet)
   #assert new.duration.target == Rational(5, 24)
   #assert len(new) == 1
   #assert new[0].duration.preprolated == Rational(1, 4)
   #assert new[0].duration.prolated == Rational(5, 24)
   assert isinstance(new, Note)
   parent = new.parentage.parent
   assert isinstance(parent, _Tuplet)
   assert parent.duration.prolated == Rational(5, 24)
   assert len(parent) == 2
   assert parent[0].duration.written == Rational(1, 4)
   assert parent[1].duration.written == Rational(1, 16)


def test_clonewp_by_duration_with_parentage_10( ):
   '''Start-to-mid jagged. '''
   t = Note(0, (1, 4))
   new = clonewp.by_duration_with_parentage(t, 0, (1, 5))
   #assert isinstance(new, FixedDurationTuplet)
   assert isinstance(new, Note)
   parent = new.parentage.parent
   assert isinstance(parent, _Tuplet)
   assert len(parent) == 1
   assert parent.duration.prolated == Rational(1, 5)
   assert parent[0].duration.preprolated == Rational(1, 4)
   assert parent[0].duration.prolated == Rational(1, 5)
