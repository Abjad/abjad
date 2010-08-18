from abjad import *


def test_FixedMultiplierTuplet_01( ):
   '''Init typical fmtuplet.'''
   
   u = Tuplet((2, 3), Note(0, (1, 8)) * 3)
   assert repr(u) == "Tuplet(2/3, [c'8, c'8, c'8])" 
   assert str(u) == "{* 3:2 c'8, c'8, c'8 *}"
   assert len(u) == 3
   assert u.duration.multiplier == Rational(2, 3)
   assert u.duration.preprolated == Rational(1, 4)
   assert u.duration.prolated == Rational(1, 4)


def test_FixedMultiplierTuplet_02( ):
   '''Init empty fmtuplet.'''

   u = Tuplet((2, 3), [ ])
   assert repr(u) == 'Tuplet(2/3, [ ])'
   assert str(u) == '{* 2/3 *}'
   assert len(u) == 0
   assert u.duration.preprolated == 0
   assert u.duration.multiplier == Rational(2, 3)
   assert u.duration.prolated == 0


def test_FixedMultiplierTuplet_03( ):
   '''Nest fmtuplet.'''

   u = Tuplet((2, 3), [
      Tuplet((4, 5), Note(0, (1, 16)) * 5),
      Note(0, (1, 4)),
      Note(0, (1, 4))])
   assert repr(u) == "Tuplet(2/3, [{* 5:4 c'16, c'16, c'16, c'16, c'16 *}, c'4, c'4])"
   assert str(u) == "{* 3:2 {* 5:4 c'16, c'16, c'16, c'16, c'16 *}, c'4, c'4 *}"
   assert len(u) == 3
   assert u.duration.preprolated == Rational(1, 2)
   assert u.duration.multiplier == Rational(2, 3)
   assert u.duration.prolated == Rational(1, 2)
   assert repr(u[0]) == "Tuplet(4/5, [c'16, c'16, c'16, c'16, c'16])"
   assert str(u[0]) == "{* 5:4 c'16, c'16, c'16, c'16, c'16 *}"
   assert len(u[0]) == 5
   assert u[0].duration.preprolated == Rational(1, 4)
   assert u[0].duration.multiplier == Rational(4, 5)
   assert u[0].duration.prolated == Rational(1, 6)


def test_FixedMultiplierTuplet_04( ):
   '''Nest empty fmtuplet.'''

   u = Tuplet((2, 3), [
      Tuplet((4, 5), [ ]),
      Note(0, (1, 4)),
      Note(0, (1, 4))])
   assert repr(u) == "Tuplet(2/3, [{* 4/5 *}, c'4, c'4])"
   assert str(u) == "{* 3:2 {* 4/5 *}, c'4, c'4 *}"
   assert len(u) == 3
   assert u.duration.preprolated == Rational(1, 3)
   assert u.duration.multiplier == Rational(2, 3)
   assert u.duration.prolated == Rational(1, 3)
   assert repr(u[0]) == 'Tuplet(4/5, [ ])'
   assert str(u[0]) == '{* 4/5 *}'
   assert len(u[0]) == 0
   assert u[0].duration.preprolated == Rational(0)
   assert u[0].duration.multiplier == Rational(4, 5)
   assert u[0].duration.prolated == Rational(0)
