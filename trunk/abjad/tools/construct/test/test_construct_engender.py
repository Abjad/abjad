from abjad import *


def test_construct_engender_01( ):
   '''Empty list, tuple or set engenders a rest.'''
   t = construct.engender([ ], (1, 4))
   assert isinstance(t, Rest)
   assert t.signature == (( ), (1, 4))
   t = construct.engender(( ), (1, 4))
   assert isinstance(t, Rest)
   assert t.signature == (( ), (1, 4))
   t = construct.engender(set([ ]), (1, 4))
   assert isinstance(t, Rest)
   assert t.signature == (( ), (1, 4))


def test_construct_engender_02( ):
   '''One-element list, tuple or set engenders a note.'''
   t = construct.engender([('c', 4)], (1, 4))
   assert isinstance(t, Note)
   assert t.signature == ((('c', 4), ), (1, 4))
   t = construct.engender((('c', 4), ), (1, 4))
   assert isinstance(t, Note)
   assert t.signature == ((('c', 4), ), (1, 4))
   t = construct.engender(set([('c', 4)]), (1, 4))
   assert isinstance(t, Note)
   assert t.signature == ((('c', 4), ), (1, 4))


def test_construct_engender_03( ):
   '''Multielement list, tuple or set engenders a chord.'''
   t = construct.engender([('c', 4), ('e', 4), ('f', 4)], (1, 4))
   assert isinstance(t, Chord)
   assert t.signature == ((('c', 4), ('e', 4), ('f', 4)), (1, 4))
   t = construct.engender((('c', 4), ('e', 4), ('f', 4)), (1, 4))
   assert isinstance(t, Chord)
   assert t.signature == ((('c', 4), ('e', 4), ('f', 4)), (1, 4))
   t = construct.engender(set([('c', 4), ('e', 4), ('f', 4)]), (1, 4))
   assert isinstance(t, Chord)
   assert t.signature == ((('c', 4), ('e', 4), ('f', 4)), (1, 4))
