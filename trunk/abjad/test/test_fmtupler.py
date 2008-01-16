from abjad import *


### INIT TYPICAL FMTUPLET ###

def test_init_typical_fmtuplet( ):
   
   u = FixedMultiplierTuplet((2, 3), Note(0, (1, 8)) * 3)
   assert repr(u) == "FixedMultiplierTuplet(2/3, [c'8, c'8, c'8])" 
   assert str(u) == "{* 3:2 c'8, c'8, c'8 *}"
   assert len(u) == 3
   assert u.multiplier == Rational(2, 3)
   assert u.duration == Duration(1, 4)
   assert u.duratum == Duration(1, 4)


#### INIT EMPTY FMTUPLET ###
#
#def test_empty_fmtuplet( ):
#
#   u = FixedMultiplierTuplet( )
#   assert repr(u) == 'FixedMultiplierTuplet( )'
#   assert str(u) == '{*}'
#   assert len(u) == 0
#   assert u.multiplier == None
#   assert u.duration == None
#   assert u.duratum == None
#
#
#### INIT EMPTY FMTUPLET, THEN SET MULTIPLIER ###
#
#def test_init_empty_fmtuplet_then_set_multiplier( ):
#
#   u = FixedMultiplierTuplet( )
#   u.multiplier = (2, 3)
#   assert repr(u) == 'FixedMultiplierTuplet(2/3)'
#   assert str(u) == '{3:2 *}'
#   assert len(u) == 0
#   assert u.multiplier == Rational(2, 3)
#   assert u.duration == None
#   assert u.duratum == None
#
#
#### INIT EMPTY FMTUPLET, THEN EXTEND MUSIC ###
#
#def test_init_empty_fmtuplet_then_extend_music( ):
#
#   u = FixedMultiplierTuplet( )
#   u.extend(Note(0, (1, 8)) * 3)
#   assert repr(u) == "FixedMultiplierTuplet(c'8, c'8, c'8)"
#   assert str(u) == "{c'8, c'8, c'8 *}"
#   assert len(u) == 3
#   assert u.multiplier == None
#   assert u.duration == None
#   assert u.duratum == None


### INIT EMPTY FMTUPLET (ALTERNATIVE) ###

def test_empty_fmtuplet( ):

   u = FixedMultiplierTuplet((2, 3), [ ])
   assert repr(u) == 'FixedMultiplierTuplet(2/3, [ ])'
   assert str(u) == '{* 2/3 *}'
   assert len(u) == 0
   assert u.duration == Duration(0)
   assert u.multiplier == Rational(2, 3)
   assert u.duratum == Duration(0)


### NEST TYPICAL FMTUPLET ###

def test_nest_typical_fmtuplet( ):

   u = FixedMultiplierTuplet((2, 3), [
      FixedMultiplierTuplet((4, 5), Note(0, (1, 16)) * 5),
      Note(0, (1, 4)),
      Note(0, (1, 4))])
   assert repr(u) == "FixedMultiplierTuplet(2/3, [{* 5:4 c'16, c'16, c'16, c'16, c'16 *}, c'4, c'4])"
   assert str(u) == "{* 3:2 {* 5:4 c'16, c'16, c'16, c'16, c'16 *}, c'4, c'4 *}"
   assert len(u) == 3
   assert u.duration == Duration(1, 2)
   assert u.multiplier == Rational(2, 3)
   assert u.duratum == Duration(1, 2)
   assert repr(u[0]) == "FixedMultiplierTuplet(4/5, [c'16, c'16, c'16, c'16, c'16])"
   assert str(u[0]) == "{* 5:4 c'16, c'16, c'16, c'16, c'16 *}"
   assert len(u[0]) == 5
   assert u[0].duration == Duration(1, 4)
   assert u[0].multiplier == Rational(4, 5)
   assert u[0].duratum == Duration(1, 6)


### NEST EMPTY FMTUPLET ###

def test_nest_typical_fmtuplet( ):

   u = FixedMultiplierTuplet((2, 3), [
      FixedMultiplierTuplet((4, 5), [ ]),
      Note(0, (1, 4)),
      Note(0, (1, 4))])
   assert repr(u) == "FixedMultiplierTuplet(2/3, [{* 4/5 *}, c'4, c'4])"
   assert str(u) == "{* 3:2 {* 4/5 *}, c'4, c'4 *}"
   assert len(u) == 3
   assert u.duration == Duration(1, 3)
   assert u.multiplier == Rational(2, 3)
   assert u.duratum == Duration(1, 3)
   assert repr(u[0]) == 'FixedMultiplierTuplet(4/5, [ ])'
   assert str(u[0]) == '{* 4/5 *}'
   assert len(u[0]) == 0
   assert u[0].duration == Duration(0)
   assert u[0].multiplier == Rational(4, 5)
   assert u[0].duratum == Duration(0)
