from abjad import *
from abjad.checks import ContainersEmpty
checker = ContainersEmpty( )
import py.test


def test_measure_empty_01( ):
   t = RigidMeasure(None, [ ])
   assert repr(t) == 'RigidMeasure( )'
   assert str(t) == '| |'
   assert py.test.raises(UnderfullMeasureError, 't.format')
   assert t.meter.forced == None
   assert len(t) == 0
   assert t.duration.preprolated == Rational(0)
   assert t.duration.prolated == Rational(0)
   assert not checker.check(t)


def test_measure_empty_02( ):
   t = RigidMeasure((4, 4), [ ])
   assert repr(t) == 'RigidMeasure(4/4)'
   assert str(t) == '|4/4|'
   assert py.test.raises(UnderfullMeasureError, 't.format')
   assert len(t) == 0
   assert t.duration.preprolated == 0
   assert t.duration.prolated == 0
   assert not checker.check(t)


def test_measure_empty_03( ):
   t = RigidMeasure((4, 5), [ ])
   assert repr(t) == 'RigidMeasure(4/5)'
   assert str(t) == '|4/5|'
   assert py.test.raises(UnderfullMeasureError, 't.format')
   assert len(t) == 0
   assert t.duration.preprolated == 0
   assert t.duration.prolated == 0
   assert not checker.check(t)
