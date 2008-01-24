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
      Leaf.grace.before accepts None.'''
   t = Note(0, (1, 4))
   t.grace.before = None
   assert t.format == "c'4"


def test_grace_03( ):
   '''Leaf.grace.before accepts any single leaf.'''
   t = Note(0, (1, 4))
   t.grace.before = Note(2, (1, 16))
   assert t.format == "\\grace {\n\td'16\n}\nc'4"
   '''
   \grace {
           d'16
   }
   c'4
   '''


def test_grace_04( ):
   '''Leaf.grace.before accepts any single grace.'''
   t = Note(0, (1, 4))
   t.grace.before = Grace([Note(2, (1, 16))])
   assert t.format == "\\grace {\n\td'16\n}\nc'4"
   '''
   \grace {
           d'16
   }
   c'4
   '''


def test_grace_05( ):
   '''Leaf.grace.before accepts a list or tuple of grace music.'''
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

def test_grace_06( ):
   '''Leaf.grace.before accepts string descriptors: "grace", "acciaccatura", "appoggiatura" when grace.before != None'''
   t = Note(0, (1, 4)) 
   t.grace.before = Note(2, (1, 16))
   assert t.grace.before
   t.grace.before = 'appoggiatura'
   assert t.format == "\\appoggiatura {\n\td'16\n}\nc'4"
   '''
   \appoggiatura {
           d'16
   }
   c'4
   '''
   t.grace.before = 'grace'
   assert t.format == "\\grace {\n\td'16\n}\nc'4"
   '''
   \grace {
           d'16
   }
   c'4
   '''
   t.grace.before = 'acciaccatura'
   assert t.format == "\\acciaccatura {\n\td'16\n}\nc'4"
   '''
   \acciaccatura {
           d'16
   }
   c'4
   '''

 
def test_grace_07( ):
   '''Leaf.grace.after accepts None.'''
   t = Note(0, (1, 4))
   t.grace.after = None
   assert t.format == "c'4"


def test_grace_08( ):
   '''Leaf.grace.after accepts any single leaf.'''
   t = Note(0, (1, 4))
   t.grace.after = Note(2, (1, 16))
   assert t.format == "\\afterGrace\nc'4\n{\n\td'16\n}"
   '''
   \afterGrace
   c'4
   {
           d'16
   }
   '''

def test_grace_09( ):
   '''Leaf.grace.after accepts any single grace.'''
   t = Note(0, (1, 4))
   t.grace.after = Grace([Note(2, (1, 16))])
   assert t.format == "\\afterGrace\nc'4\n{\n\td'16\n}"
   '''
   \afterGrace
   c'4
   {
           d'16
   }
   '''


def test_grace_10( ):
   '''Leaf.grace.after accepts a list or tuple of grace music.'''
   t = Note(0, (1, 4))
   t.grace.after = [Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))]
   assert t.format =="\\afterGrace\nc'4\n{\n\tc'16\n\td'16\n\te'16\n}"
    
   '''
   \afterGrace
   c'4
   {
           c'16
           d'16
           e'16
   }
   '''
