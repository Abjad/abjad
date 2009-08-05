from abjad import *


## TEST NEST TYPICAL FDTUPLET ##

def test_nest_typical_fdtuplet( ):
   
   t = FixedDurationTuplet((2, 4), [
      FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3),
      Note(0, (1, 8)),
      Note(0, (1, 8)),
      Note(0, (1, 8))])
   assert repr(t) == "FixedDurationTuplet(1/2, [{@ 3:2 c'8, c'8, c'8 @}, c'8, c'8, c'8])"
   assert str(t) == "{@ 5:4 {@ 3:2 c'8, c'8, c'8 @}, c'8, c'8, c'8 @}"
   assert t.duration.target == Rational(1, 2)
   assert t.duration.multiplier == Rational(4, 5)
   assert t.duration.prolated == Rational(1, 2)
   assert repr(t[0]) == "FixedDurationTuplet(1/4, [c'8, c'8, c'8])"
   assert str(t[0]) == "{@ 3:2 c'8, c'8, c'8 @}"
   assert len(t[0]) == 3
   assert t[0].duration.target == Rational(1, 4)
   assert t[0].duration.multiplier == Rational(2, 3)
   assert t[0].duration.prolated == Rational(1, 5)


## TEST NEST EMPTY FDTUPLET ##

def test_nest_typical_fdtuplet( ):
   
   t = FixedDurationTuplet((2, 4), [
      FixedDurationTuplet((2, 8), [ ]),
      Note(0, (1, 8)),
      Note(0, (1, 8)),
      Note(0, (1, 8))])
   assert repr(t) == "FixedDurationTuplet(1/2, [{@ 1/4 @}, c'8, c'8, c'8])"
   assert str(t) == "{@ 5:4 {@ 1/4 @}, c'8, c'8, c'8 @}"
   assert t.duration.target == Rational(1, 2)
   assert t.duration.multiplier == Rational(4, 5)
   assert t.duration.prolated == Rational(1, 2)
   assert repr(t[0]) == 'FixedDurationTuplet(1/4, [ ])'
   assert str(t[0]) == '{@ 1/4 @}'
   assert len(t[0]) == 0
   assert t[0].duration.target == Rational(1, 4)
   assert t[0].duration.multiplier == None
   assert t[0].duration.prolated == Rational(1, 5)


## TEST 1-MULTIPLIER TUPLET ##

def test_1_multiplier_tuplet_01( ):
   t = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 2)
   assert repr(t) == "FixedDurationTuplet(1/4, [c'8, c'8])"
   assert str(t) == "{@ 1:1 c'8, c'8 @}"
   assert t.format == "\tc'8\n\tc'8"


def test_1_mutliplier_tuplet_02( ):
   t = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   t.pop( )
   assert repr(t) == "FixedDurationTuplet(1/4, [c'8, c'8])"
   assert str(t) == "{@ 1:1 c'8, c'8 @}"
   assert t.format == "\tc'8\n\tc'8"


def test_invisible_tuplet( ):
   '''Tuplet.invisible formats compressed music.'''
   t = FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)
   assert t.invisible == False
   t.invisible = True
   assert t.format == "\\scaleDurations #'(2 . 3) {\n\tc'8\n\tc'8\n\tc'8\n}"
   r'''
   \scaleDurations #'(2 . 3) {
      c'8
      c'8
      c'8
   }
   '''
   t.invisible = False
   assert t.format == "\\times 2/3 {\n\tc'8\n\tc'8\n\tc'8\n}"
