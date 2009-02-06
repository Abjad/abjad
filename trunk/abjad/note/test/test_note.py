from abjad import *
from py.test import raises


### TEST OCTAVE ZERO ###

def test_octave_zero_01( ):
   '''Notes print correctly when pitch is in octave 0.'''
   t = Note(-37, (1, 4))
   assert t.format == 'b,,,4'


### ASSERTS ###

def test_assert_duration_is_notehead_assignable_01( ):
   #raises(ValueError, Note, 0, (5, 8))
   raises(AssignabilityError, 'Note(0, (5, 8))')
