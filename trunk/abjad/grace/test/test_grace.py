from abjad import *
import py.test


def test_grace_01( ):
   '''Grace music is a container.'''

   t = Grace([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])

   assert isinstance(t, Container)
   assert len(t) == 3
   assert t.format == "\\grace {\n\tc'16\n\td'16\n\te'16\n}"

   r'''\grace {
           c'16
           d'16
           e'16
   }'''


def test_grace_02( ):
   '''Grace.kind is managed attribute. 
      Grace.kind knows about "after", "grace", 
      "acciaccatura", "appoggiatura"'''

   t = Grace([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])
   t.kind = 'acciaccatura'
   assert t.kind == 'acciaccatura'
   t.kind = 'grace'
   assert t.kind == 'grace'
   t.kind = 'after'
   assert t.kind == 'after'
   t.kind = 'appoggiatura'
   assert t.kind == 'appoggiatura'
   assert py.test.raises(AssertionError, 't.kind = "blah"')
   

def test_grace_03( ):
   '''Grace formats correctly as grace.'''

   t = Grace(construct.run(3))
   t.kind = 'grace'
   assert t.format == "\\grace {\n\tc'8\n\tc'8\n\tc'8\n}"

   r'''\grace {
           c'8
           c'8
           c'8
   }'''


def test_grace_04( ):
   '''Grace formats correctly as acciaccatura.'''

   t = Grace(construct.run(3))
   t.kind = 'acciaccatura'
   assert t.format == "\\acciaccatura {\n\tc'8\n\tc'8\n\tc'8\n}"

   r'''\acciaccatura {
           c'8
           c'8
           c'8
   }'''


def test_grace_05( ):
   '''Grace formats correctly as appoggiatura.'''

   t = Grace(construct.run(3))
   t.kind = 'appoggiatura'
   assert t.format == "\\appoggiatura {\n\tc'8\n\tc'8\n\tc'8\n}"

   r'''\appoggiatura {
           c'8
           c'8
           c'8
   }'''


def test_grace_06( ):
   '''Grace formats correctly as after grace.'''

   t = Grace(construct.run(3))
   t.kind = 'after'
   assert t.format == "{\n\tc'8\n\tc'8\n\tc'8\n}"

   r'''{
           c'8
           c'8
           c'8
   }'''


def test_grace_07( ):
   '''Grace containers can be appended.'''

   t = Grace(construct.run(2))
   n = Note(1, (1, 4))
   t.append(n)
   assert len(t) == 3
   assert t[-1] is n


def test_grace_08( ):
   '''Grace containers can be extended.'''

   t = Grace(construct.run(2))
   ns = Note(1, (1, 4)) * 2
   t.extend(ns)
   assert len(t) == 4
   assert t[-2:] == ns
