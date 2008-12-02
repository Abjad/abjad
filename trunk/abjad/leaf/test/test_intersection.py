from abjad import *


### TODO: decide what happens when one or the other chord is *spanned*;
###       then write some tests to lock in that behavior.

def test_intersection_01( ):
   '''Chords completely disjunct;
      empty set returned as skip.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([3, 4, 5], (1, 4))
   v = t & u
   assert isinstance(v, Skip)
   assert v.signature == (( ), (1, 4))
   assert t is not u is not v


def test_intersection_02( ):
   '''Partially intersecting chords;
      multiple shared pitches return as chord.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([1, 2, 3], (1, 4))
   v = t & u
   assert isinstance(v, Chord)
   assert v.signature == ((('cs', 4), ('d', 4)), (1, 4))
   assert t is not u is not v


def test_intersection_03( ):
   '''Wholly intersecting chords;
      shared pitches appear only once.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([0, 1, 2], (1, 4))
   v = t & u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('cs', 4), ('d', 4)), (1, 4))
   assert t is not u is not v
   

def test_intersection_04( ):
   '''Enharmonically disjunct;
      enharmonic equivalents do not appear.'''
   t = Chord([0, ('cs', 4), 2], (1, 4))
   u = Chord([0, ('df', 4), 2], (1, 4))
   v = t & u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('d', 4)), (1, 4))
   assert t is not u is not v


def test_intersection_05( ):
   '''Duration inequality;
      noncommutative union takes from LHS.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([1, 2, 3], (1, 8))
   v = t & u
   assert isinstance(v, Chord)
   assert v.signature == ((('cs', 4), ('d', 4)), (1, 4))
   assert v.duration.written.pair == t.duration.written.pair
   assert t is not u is not v


def test_intersection_06( ):
   '''Duration inequality;
      noncommutative union takes from LHS.'''
   t = Chord([0, 1, 2], (1, 8))
   u = Chord([1, 2, 3], (1, 4))
   v = t & u
   assert isinstance(v, Chord)
   assert v.signature == ((('cs', 4), ('d', 4)), (1, 8))
   assert v.duration.written.pair == t.duration.written.pair
   assert t is not u is not v


def test_intersection_07( ):
   '''Partially intersecting chords;
      one shared pitch returns as note.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([2, 3, 4], (1, 4))
   v = t & u
   assert isinstance(v, Note)
   assert v.signature == ((('d', 4), ), (1, 4))
   assert t is not u is not v


