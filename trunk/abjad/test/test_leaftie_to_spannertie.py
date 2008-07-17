from abjad import *
from abjad.helpers.leaftie_to_spannertie import _leaftie_to_spannertie
from py.test import raises

def test_leaftie_to_spannertie_01( ):
   t = Note(1, (1, 4))
   t.tie = True
   _leaftie_to_spannertie(t)
   assert t.tie == False
   assert t.tie.spanner

def test_leaftie_to_spannertie_02( ):
   '''Leaftie to spannertie works on single leaf inside Container.'''
   t = Voice(Note(1, (1, 4)) * 4)
   for n in t[:-1]:
      n.tie = True
   _leaftie_to_spannertie(t[-1])
   sp = t[0].tie.spanner
   for n in t:
      assert n.tie == False
      assert n.tie.spanner
      assert n.tie.spanner is sp

def test_leaftie_to_spannertie_03( ):
   '''Leaftie to spannertie works on Container with one tied duration.'''
   t = Voice(Note(1, (1, 4)) * 4)
   for n in t[:-1]:
      n.tie = True
   _leaftie_to_spannertie(t)
   sp = t[0].tie.spanner
   for n in t:
      assert n.tie == False
      assert n.tie.spanner
      assert n.tie.spanner is sp

def test_leaftie_to_spannertie_04( ):
   '''Leaftie to spannertie works on Container with multiple ties.'''
   t = Voice(Note(1, (1, 4)) * 8)
   for n in t[0:2]:
      n.tie = True
   for n in t[5:8]:
      n.tie = True
   _leaftie_to_spannertie(t)
   sp = t[0].tie.spanner
   for n in t[0:2]:
      assert n.tie == False
      assert n.tie.spanner
      assert n.tie.spanner is sp
   sp = t[-1].tie.spanner
   for n in t[5:8]:
      assert n.tie == False
      assert n.tie.spanner
      assert n.tie.spanner is sp
   assert not t[3].tie.isTied( )
   assert not t[4].tie.isTied( )

