from abjad import *
from py.test import raises


def test_grace_01( ):
   '''Grace music is a container.'''
   t = Grace([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])
   assert t.kind('Container')
   assert len(t) == 3
   assert t.format == "\\grace {\n\tc'16\n\td'16\n\te'16\n}"
   '''
   \grace {
           c'16
           d'16
           e'16
   }
   '''


def test_grace_02( ):
   '''
   Grace.type is managed attribute. 
   Grace.type knows about "after", "grace", "acciaccatura", "appoggiatura" 
   '''
   t = Grace([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])
   t.type = 'acciaccatura'
   assert t.type == 'acciaccatura'
   t.type = 'grace'
   assert t.type == 'grace'
   t.type = 'after'
   assert t.type == 'after'
   t.type = 'appoggiatura'
   assert t.type == 'appoggiatura'
   assert raises(AssertionError, 't.type = "blah"')
   

### FORMAT ###

def test_grace_03( ):
   '''Grace formats correctly as grace.'''
   t = Grace(run(3))
   t.type = 'grace'
   assert t.format == "\\grace {\n\tc'8\n\tc'8\n\tc'8\n}"
   '''
   \grace {
           c'8
           c'8
           c'8
   }
   '''


def test_grace_04( ):
   '''Grace formats correctly as acciaccatura.'''
   t = Grace(run(3))
   t.type = 'acciaccatura'
   assert t.format == "\\acciaccatura {\n\tc'8\n\tc'8\n\tc'8\n}"
   '''
   \acciaccatura {
           c'8
           c'8
           c'8
   }
   '''


def test_grace_05( ):
   '''Grace formats correctly as appoggiatura.'''
   t = Grace(run(3))
   t.type = 'appoggiatura'
   assert t.format == "\\appoggiatura {\n\tc'8\n\tc'8\n\tc'8\n}"
   '''
   \appoggiatura {
           c'8
           c'8
           c'8
   }
   '''


def test_grace_06( ):
   '''Grace formats correctly as after grace.'''
   t = Grace(run(3))
   t.type = 'after'
   assert t.format == "{\n\tc'8\n\tc'8\n\tc'8\n}"
   '''
   {
           c'8
           c'8
           c'8
   }
   '''
