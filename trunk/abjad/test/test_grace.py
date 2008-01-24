from abjad import *


def test_grace_01( ):
   '''Grace music is a container.'''
   t = Grace([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])
   assert len(t) == 3
   assert t.duration == Duration(3, 16)
   assert t.format == "\\grace {\n\tc'16\n\td'16\n\te'16\n}"
   '''
   \grace {
           c'16
           d'16
           e'16
   }
   '''
   

def test_grace_02( ):
   '''Leaves implement a managed grace attribute;
      Leaf.grace accepts None.'''
   t = Note(0, (1, 4))
   t.grace.before = None
   assert t.format == "c'4"


def test_grace_03( ):
   '''Leaf.grace accepts any single leaf.'''
   t = Note(0, (1, 4))
   t.grace.before = Note(2, (1, 16))
   assert t.format == "\\grace {\n\td'16\n}\nc'4"
   '''
   \grace {
           c'16
   }
   c'4
   '''


def test_grace_04( ):
   '''Leaf.grace accepts any single grace.'''
   t = Note(0, (1, 4))
   t.grace.before = Grace([Note(2, (1, 16))])
   assert t.format == "\\grace {\n\td'16\n}\nc'4"
   '''
   \grace {
           c'16
   }
   c'4
   '''


def test_grace_05( ):
   '''Leaf.grace accepts a list or tuple of grace music.'''
   t = Note(0, (1, 4))
   t.grace.before = [Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))]
   assert t.format == "\\grace {\n\tc'16\n\td'16\n\te'16\n}\nc'4"
   '''
   \grace {
           c'16
           d'16
           e'16
   }
   c'4
   '''
