from abjad import *


## DEPRECATED because ties now model exclusively with the Tie spanner

#def test_tie_spanner_01( ):
#   '''Tie spanner knows how to capture leaf ties around it.'''
#   t = Voice(Note(0, (1, 4)) * 8)
#   sp = Tie(t[4:6])
#   t[3].tie = True
#   t[6].tie = True
#   sp._captureLeafTies( )
#   assert not t[3].tie
#   assert not t[6].tie 
#   assert t[3].tie.spanner ==  t[6].tie.spanner == sp
#
#
#def test_tie_spanner_02( ):
#   '''Tie spanner know how to capture leaf ties around it.'''
#   t = Voice(Note(0, (1, 4)) * 8)
#   sp = Tie(t[4:6])
#   t[2].tie = True
#   t[3].tie = True
#   t[6].tie = True
#   t[7].tie = True
#   sp._captureLeafTies( )
#   for l in t[2:8]:
#      assert l.tie == False
#      assert l.tie.spanner == sp
#
#
#def test_tie_spanner_03( ):
#   '''Tie spanner know how to capture leaf ties around it.
#      Leaf ties not contiguous are not captured.'''
#   t = Voice(Note(0, (1, 4)) * 8)
#   sp = Tie(t[4:6])
#   t[1].tie = True
#   t[2].tie = True
#   sp._captureLeafTies( )
#   assert not t[0].tie
#   assert t[1].tie 
#   assert t[2].tie 
#   assert not t[3].tie 
#   assert not t[3].tie.spanned
#   assert t[4].tie.spanner ==  t[5].tie.spanner == sp
#   assert not t[6].tie.spanned
