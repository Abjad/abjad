from abjad import *


def test_grace_carrierage_01( ):
   '''Lone Grace containers _carrier is None.'''
   t = Grace(construct.run(4))
   assert t._carrier is None


def test_grace_carrierage_02( ):
   '''Grace containers in Leaf do have parent.'''
   t = Note(1, (1, 4))
   assert isinstance(t.grace.before, Grace)
   assert t.grace.before._carrier is t
   assert t.grace.after._carrier is t


def test_grace_carrierage_03( ):
   '''
   Grace containers in Leaf have their correct parent after assignment 
   via GraceInterface.
   '''
   t = Note(1, (1, 4))
   t.grace.after = Note(4, (1, 16))
   t.grace.before = Note(4, (1, 16))
   assert t.grace.after._carrier is t
   assert t.grace.before._carrier is t
   t.grace.after = Grace(construct.scale(2))
   t.grace.before = Grace(construct.scale(2))
   assert t.grace.after._carrier is t
   assert t.grace.before._carrier is t
   t.grace.after = None
   t.grace.before = None
   assert t.grace.after._carrier is t
   assert t.grace.before._carrier is t


def test_grace_carrierage_04( ):
   '''
   Grace container in Leaf have their correct parent after Leaf casting.
   '''
   n = Note(1, (1, 4))
   t = Rest(n)
   assert isinstance(t, Rest)
   assert t.grace.after._carrier is t
   assert t.grace.before._carrier is t
   t = Skip(n)
   assert isinstance(t, Skip)
   assert t.grace.after._carrier is t
   assert t.grace.before._carrier is t
   t = Chord(n)
   assert isinstance(t, Chord)
   assert t.grace.after._carrier is t
   assert t.grace.before._carrier is t
   t = Note(n)
   assert isinstance(t, Note)
   assert t.grace.after._carrier is t
   assert t.grace.before._carrier is t


#def test_grace_parentage_01( ):
#   '''Lone Grace containers _parent is None.'''
#   t = Grace(construct.run(4))
#   assert t._parent is None
#
#
#def test_grace_parentage_02( ):
#   '''Grace containers in Leaf do have parent.'''
#   t = Note(1, (1, 4))
#   assert isinstance(t.grace.before, Grace)
#   assert t.grace.before._parent is t
#   assert t.grace.after._parent is t
#
#
#def test_grace_parentage_03( ):
#   '''
#   Grace containers in Leaf have their correct parent after assignment 
#   via GraceInterface.
#   '''
#   t = Note(1, (1, 4))
#   t.grace.after = Note(4, (1, 16))
#   t.grace.before = Note(4, (1, 16))
#   assert t.grace.after._parent is t
#   assert t.grace.before._parent is t
#   t.grace.after = Grace(construct.scale(2))
#   t.grace.before = Grace(construct.scale(2))
#   assert t.grace.after._parent is t
#   assert t.grace.before._parent is t
#   t.grace.after = None
#   t.grace.before = None
#   assert t.grace.after._parent is t
#   assert t.grace.before._parent is t
#
#
#def test_grace_parentage_04( ):
#   '''
#   Grace container in Leaf have their correct parent after Leaf casting.
#   '''
#   n = Note(1, (1, 4))
#   t = Rest(n)
#   assert isinstance(t, Rest)
#   assert t.grace.after._parent is t
#   assert t.grace.before._parent is t
#   t = Skip(n)
#   assert isinstance(t, Skip)
#   assert t.grace.after._parent is t
#   assert t.grace.before._parent is t
#   t = Chord(n)
#   assert isinstance(t, Chord)
#   assert t.grace.after._parent is t
#   assert t.grace.before._parent is t
#   t = Note(n)
#   assert isinstance(t, Note)
#   assert t.grace.after._parent is t
#   assert t.grace.before._parent is t
