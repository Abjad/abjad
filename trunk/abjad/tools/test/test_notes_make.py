from abjad import *
from abjad.tools import construct

def test_construct_note_01( ):
   t = construct.note(1, (1,4))
   assert isinstance(t, list)
   assert len(t) == 1
   assert isinstance(t[0], Note)
   #assert t[0] == Note(1, (1,4)) this SHOULD work... __eq__ problem. 
   # check attributes independently instead.
   assert t[0].duration.written == Rational(1, 4)
   assert not t[0].tie.spanned

def test_construct_note_02( ):
   '''Tied durations result in more than one tied Note.'''
   t = construct.note(1, (5, 8))
   assert len(t) == 2
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Note)
   assert t[0].duration.written == Rational(4, 8)
   assert t[1].duration.written == Rational(1, 8)
   assert t[0].tie.spanned
   assert t[1].tie.spanned
