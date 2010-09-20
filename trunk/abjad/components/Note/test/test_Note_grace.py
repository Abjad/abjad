from abjad import *


#def test_Note_grace_01( ):
#   '''GraceInterface has a private client.'''
#   t = Note(0, (1, 4))
#   assert t.grace._client is t


#def test_Note_grace_02( ):
#   '''Leaves implement a managed grace attribute;
#      _Leaf.grace.before accepts None.'''
#   t = Note(0, (1, 4))
#   t.grace.before = None
#   assert t.format == "c'4"


def test_Note_grace_03( ):
   '''_Leaf.grace.before accepts any single leaf.'''
   t = Note(0, (1, 4))
   #t.grace.before = Note(2, (1, 16))
   t.grace.append(Note(2, (1, 16)))
   assert t.format == "\\grace {\n\td'16\n}\nc'4"
   '''
   \grace {
           d'16
   }
   c'4
   '''


#def test_Note_grace_04( ):
#   '''_Leaf.grace.before accepts any single grace.'''
#   t = Note(0, (1, 4))
#   t.grace.before = gracetools.Grace([Note(2, (1, 16))])
#   assert t.format == "\\grace {\n\td'16\n}\nc'4"
#   '''
#   \grace {
#           d'16
#   }
#   c'4
#   '''


def test_Note_grace_05( ):
   '''_Leaf.grace.before accepts a list or tuple of grace music.'''
   t = Note(0, (1, 4))
   #t.grace.before = [Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))]
   t.grace.extend([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])
   assert t.format == "\\grace {\n\tc'16\n\td'16\n\te'16\n}\nc'4"
   '''
   \grace {
           c'16
           d'16
           e'16
   }
   c'4
   '''

def test_Note_grace_06( ):
   '''_Leaf.grace.before accepts string descriptors: "grace", "acciaccatura", "appoggiatura" '''

   t = Note(0, (1, 4)) 
   #t.grace.before = Note(2, (1, 16))
   #t.grace.before = 'appoggiatura'
   t.grace.append(Note(2, (1, 16)))
   t.grace.kind = 'appoggiatura'
   assert t.format == "\\appoggiatura {\n\td'16\n}\nc'4"
   r'''
   \appoggiatura {
           d'16
   }
   c'4
   '''
   #t.grace.before = 'grace'
   t.grace.kind = 'grace'
   assert t.format == "\\grace {\n\td'16\n}\nc'4"
   r'''
   \grace {
           d'16
   }
   c'4
   '''
   #t.grace.before = 'acciaccatura'
   t.grace.kind = 'acciaccatura'
   assert t.format == "\\acciaccatura {\n\td'16\n}\nc'4"
   r'''
   \acciaccatura {
           d'16
   }
   c'4
   '''

 
#def test_Note_grace_07( ):
#   '''_Leaf.grace.after accepts None.'''
#   t = Note(0, (1, 4))
#   t.grace.after = None
#   assert t.format == "c'4"


def test_Note_grace_08( ):
   '''_Leaf.grace.after accepts any single leaf.'''
   t = Note(0, (1, 4))
   #t.grace.after = Note(2, (1, 16))
   t.after_grace.append(Note(2, (1, 16)))
   assert t.format == "\\afterGrace\nc'4\n{\n\td'16\n}"
   r'''
   \afterGrace
   c'4
   {
           d'16
   }
   '''


#def test_Note_grace_09( ):
#   '''_Leaf.grace.after accepts any single grace.'''
#   t = Note(0, (1, 4))
#   t.grace.after = gracetools.Grace([Note(2, (1, 16))])
#   assert t.format == "\\afterGrace\nc'4\n{\n\td'16\n}"
#   '''
#   \afterGrace
#   c'4
#   {
#           d'16
#   }
#   '''


def test_Note_grace_10( ):
   '''_Leaf.grace.after accepts a list or tuple of grace music.'''
   t = Note(0, (1, 4))
   #t.grace.after = [Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))]
   t.after_grace.extend([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])
   assert t.format =="\\afterGrace\nc'4\n{\n\tc'16\n\td'16\n\te'16\n}"
    
   r'''
   \afterGrace
   c'4
   {
           c'16
           d'16
           e'16
   }
   '''
