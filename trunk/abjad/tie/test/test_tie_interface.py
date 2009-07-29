from abjad import *


#def test_tie_interface_01( ):
#   '''Tie interface tests nonzero.'''
#   t = Note(0, (3, 64))
#   assert not t.tie
#   t.tie = True
#   assert t.tie
#
#
#def test_tie_interface_02( ):
#   '''Tie interface tests eq.'''
#   t = Note(0, (3, 64))
#   assert t.tie == False
#   t.tie = True
#   assert t.tie == True


def test_tie_interface_03( ):
   '''Attributes format correcty.'''
   t = Note(0, (1, 4))
   t.tie.color = 'red'
   assert t.format == "\\once \\override Tie #'color = #red\nc'4"
  

def test_tie_interface_04( ):
   '''Clear deletes assigned attributes.'''
   t = Note(0, (1, 4))
   t.tie.color = 'red'
   assert t.format == "\\once \\override Tie #'color = #red\nc'4"
   #t.tie.clear( )
   overridetools.clear_all(t.tie)
   assert t.format == "c'4"


#def test_tie_interface_05( ):
#   '''Leaf.tied if Leaf.prev.tie.'''
#   t = Voice(Note(0, (1, 4)) * 3)
#   t[1].tie = True
#   assert not t[0].tie.tied
#   assert not t[1].tie.tied
#   assert t[2].tie.tied
#
#
#def test_tie_interface_06( ):
#   '''Leaf.tail if last in Tie spanner.'''
#   t = Voice(Note(0, (1,4)) * 3)
#   Tie(t[1:])
#   assert not t[0].tie.tail
#   assert not t[1].tie.tail
#   assert t[2].tie.tail
#
#
#def test_tie_interface_07( ):
#   '''Leaf.tail if last in chain of leaf ties.'''
#   t = Voice(Note(0, (1,4)) * 3)
#   t[0].tie = True
#   t[1].tie = True
#   assert not t[0].tie.tail
#   assert not t[1].tie.tail
#   assert t[2].tie.tail
#
#
#def test_tie_interface_08( ):
#   '''Leaf.head if first in Tie spanner.'''
#   t = Voice(Note(0, (1,4)) * 3)
#   Tie(t[1:])
#   assert not t[0].tie.head
#   assert t[1].tie.head
#   assert not t[2].tie.head
#
#
#def test_tie_interface_09( ):
#   '''Leaf.head if not Leaf.prev.tie.'''
#   t = Voice(Note(0, (1,4)) * 3)
#   t[1].tie = True
#   t[2].tie = True
#   assert not t[0].tie.head
#   assert t[1].tie.head
#   assert not t[2].tie.head
