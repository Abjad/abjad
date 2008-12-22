from abjad import *


### TEST DEMO PUBLIC OVERRIDE INTERFACE ###

def test_demo_public_override_interface_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   q = Override(t[0], 'Beam', 'positions', (8, 8))

   assert repr(q) == "Override([c'8], Beam, positions, (8, 8))"
   assert str(q) == repr(q)
   assert len(q.components) == 1
   assert q.duration == Rational(1, 8)
   assert t.format == "\\new Staff {\n\t\\once \\override Beam #'positions = #'(8 . 8)\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"

   r'''
   \new Staff {
      \once \override Beam #'positions = #'(8 . 8)
       c'8
       cs'8
       d'8
       ef'8
       e'8
       f'8
       fs'8
       g'8
   }
   '''


def test_demo_public_override_interface_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   q = Override(t[ : 4], 'Beam', 'positions', (8, 8))

   assert repr(q) == "Override([c'8, cs'8, d'8, ef'8], Beam, positions, (8, 8))"
   assert str(q) == repr(q)
   assert len(q.components) == 4
   assert q.duration == Rational(1, 2)
   assert t.format == "\\new Staff {\n\t\\override Beam #'positions = #'(8 . 8)\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\revert Beam #'positions\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"

   r'''
   \new Staff {
      \override Beam #'positions = #'(8 . 8)
       c'8
       cs'8
       d'8
       ef'8
       \revert Beam #'positions
       e'8
       f'8
       fs'8
       g'8
   }
   '''


### TEST OVERRIDE CONTAINS ###

def test_override_contains_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   q = Override(t[ : 4], 'Beam', 'positions', (8, 8))
   for x in t[ : 4]:
      assert x in q.components



### TEST OVERRIDE GETITEM ###

def test_override_getitem_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   q = Override(t[ : 4], 'Beam', 'positions', (8, 8))
   for i in range(4):
      assert q.components[i] == t[i]


def test_override_getitem_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   q = Override(t[ : 4], 'Beam', 'positions', (8, 8))
   assert q.components[1 : 3] == t[1 : 3]


def test_override_getitem_03( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   q = Override(t[ : 4], 'Beam', 'positions', (8, 8))
   assert q.components[1 : ] == t[1 : 4]


def test_override_getitem_04( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   q = Override(t[ : 4], 'Beam', 'positions', (8, 8))
   assert q.components[ : -1] == t[ : 3]
