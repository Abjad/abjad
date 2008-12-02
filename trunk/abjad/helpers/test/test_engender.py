from abjad import *


def test_engender_01( ):
   '''Empty list, tuple or set engenders a rest.'''
   t = engender([ ], (1, 4))
   assert isinstance(t, Rest)
   assert t.signature == (( ), (1, 4))
   t = engender(( ), (1, 4))
   assert isinstance(t, Rest)
   assert t.signature == (( ), (1, 4))
   t = engender(set([ ]), (1, 4))
   assert isinstance(t, Rest)
   assert t.signature == (( ), (1, 4))


def test_engender_02( ):
   '''One-element list, tuple or set engenders a note.'''
   t = engender([('c', 4)], (1, 4))
   assert isinstance(t, Note)
   assert t.signature == ((('c', 4), ), (1, 4))
   t = engender((('c', 4), ), (1, 4))
   assert isinstance(t, Note)
   assert t.signature == ((('c', 4), ), (1, 4))
   t = engender(set([('c', 4)]), (1, 4))
   assert isinstance(t, Note)
   assert t.signature == ((('c', 4), ), (1, 4))


def test_engender_03( ):
   '''Multielement list, tuple or set engenders a chord.'''
   t = engender([('c', 4), ('e', 4), ('f', 4)], (1, 4))
   assert isinstance(t, Chord)
   assert t.signature == ((('c', 4), ('e', 4), ('f', 4)), (1, 4))
   t = engender((('c', 4), ('e', 4), ('f', 4)), (1, 4))
   assert isinstance(t, Chord)
   assert t.signature == ((('c', 4), ('e', 4), ('f', 4)), (1, 4))
   t = engender(set([('c', 4), ('e', 4), ('f', 4)]), (1, 4))
   assert isinstance(t, Chord)
   assert t.signature == ((('c', 4), ('e', 4), ('f', 4)), (1, 4))
