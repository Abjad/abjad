from abjad import *
from py.test import raises


def test_grace_01( ):
   '''Grace music is a container.'''

   t = Grace([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])

   assert isinstance(t, Container)
   assert len(t) == 3
   assert t.format == "\\grace {\n\tc'16\n\td'16\n\te'16\n}"

   r'''
   \grace {
           c'16
           d'16
           e'16
   }
   '''


def test_grace_02( ):
   '''Grace.type is managed attribute. 
      Grace.type knows about "after", "grace", 
      "acciaccatura", "appoggiatura"'''

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
   

## FORMAT ##

def test_grace_03( ):
   '''Grace formats correctly as grace.'''

   t = Grace(run(3))
   t.type = 'grace'
   assert t.format == "\\grace {\n\tc'8\n\tc'8\n\tc'8\n}"

   r'''
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

   r'''
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

   r'''
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

   r'''
   {
           c'8
           c'8
           c'8
   }
   '''


## APPEND, EXTEND ##

def test_grace_10( ):
   '''Grace containers can be appended.'''

   t = Grace(run(2))
   n = Note(1, (1, 4))
   t.append(n)
   assert len(t) == 3
   assert t[-1] is n


def test_grace_11( ):
   '''Grace containers can be extended.'''

   t = Grace(run(2))
   ns = Note(1, (1, 4)) * 2
   t.extend(ns)
   assert len(t) == 4
   assert t[-2:] == ns
