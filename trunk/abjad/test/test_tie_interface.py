from abjad import *


def test_tie_interface_01( ):
   '''Tie interface tests nonzero.'''
   t = Note(0, (3, 64))
   assert not t.tie
   t.tie = True
   assert t.tie


def test_tie_interface_02( ):
   '''Tie interface tests eq.'''
   t = Note(0, (3, 64))
   assert t.tie == False
   t.tie = True
   assert t.tie == True


def test_tie_interface_03( ):
   '''Attributes format correcty.'''
   t = Note(0, (1,4))
   t.tie.color = 'red'
   assert t.format == "\\once \\override Tie #'color = #red\nc'4"
  

def test_tie_interface_04( ):
   '''Clear deletes assigned attributes.'''
   t = Note(0, (1,4))
   t.tie.color = 'red'
   assert t.format == "\\once \\override Tie #'color = #red\nc'4"
   t.tie.clear()
   assert t.format == "c'4"


