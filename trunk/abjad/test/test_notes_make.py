from abjad import *

def test_notes_make_01( ):
   t = notes_make(1, (1,4))
   assert isinstance(t, list)
   assert len(t) == 1
   assert isinstance(t[0], Note)
   #assert t[0] == Note(1, (1,4)) this SHOULD work... __eq__ problem. 
   # check attributes independently instead.
   assert t[0].duration.written == Rational(1, 4)
   assert not t[0].tie.isTied( )

def test_notes_make_02( ):
   '''Tied durations result in more than one tied Note.'''
   t = notes_make(1, (5, 8))
   assert len(t) == 2
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Note)
   assert t[0].duration.written == Rational(4, 8)
   assert t[1].duration.written == Rational(1, 8)
   assert t[0].tie.spanner
   assert t[1].tie.spanner
