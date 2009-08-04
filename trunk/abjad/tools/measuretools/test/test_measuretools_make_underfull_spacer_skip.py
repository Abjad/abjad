from abjad import *


def test_measuretools_make_underfull_spacer_skip_01( ):
   '''Handles measure prolation from nonbinary meter.'''

   t = RigidMeasure((4, 12), construct.scale(4))
   t.meter.forced = Meter(5, 12)
   assert t.duration.is_underfull

   skip = measuretools.make_underfull_spacer_skip(t)

   assert isinstance(skip, Skip)
   assert skip.duration.written == Rational(1, 1)
   assert skip.duration.multiplier == Rational(1, 8)


def test_measuretools_make_underfull_spacer_skip_02( ):
   '''Handles regular measure with no meter prolation.'''

   t = RigidMeasure((4, 8), construct.scale(4))
   t.meter.forced = Meter(5, 8)
   assert t.duration.is_underfull

   skip = measuretools.make_underfull_spacer_skip(t)

   assert isinstance(skip, Skip)
   assert skip.duration.written == Rational(1, 1)
   assert skip.duration.multiplier == Rational(1, 8)
