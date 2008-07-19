from abjad import *


def test_tie_spanner_10( ):
   '''Tie spanner know how to capture leaf ties around it.'''
   t = Voice(Note(0, (1, 4)) * 8)
   sp = Tie(t[4:6])
   t[3].tie = True
   t[6].tie = True
   sp._captureLeafTies( )
   assert t[3].tie == False
   assert t[6].tie == False
   assert t[3].tie.spanner ==  t[6].tie.spanner == sp

def test_tie_spanner_11( ):
   '''Tie spanner know how to capture leaf ties around it.'''
   t = Voice(Note(0, (1, 4)) * 8)
   sp = Tie(t[4:6])
   t[2].tie = True
   t[3].tie = True
   t[6].tie = True
   t[7].tie = True
   sp._captureLeafTies( )
   for l in t[2:8]:
      assert l.tie == False
      assert l.tie.spanner == sp


def test_tie_spanner_12( ):
   '''Tie spanner know how to capture leaf ties around it.
      Leaf ties not contiguous are not captured.'''
   t = Voice(Note(0, (1, 4)) * 8)
   sp = Tie(t[4:6])
   t[1].tie = True
   t[2].tie = True
   sp._captureLeafTies( )
   assert t[0].tie == False
   assert t[1].tie == True
   assert t[2].tie == True
   assert t[3].tie == False
   assert not t[3].tie.spanner
   assert t[4].tie.spanner ==  t[5].tie.spanner == sp
   assert not t[6].tie.isTied( )

