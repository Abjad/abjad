from abjad import *


### TODO: decide what happens when one or the other chord is *spanned*;
###       then write some tests to lock in that behavior.

def test_difference_01( ):
   '''Chords completely disjunct;
      all RH pitches preserved.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([3, 4, 5], (1, 4))
   v = t - u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('cs', 4), ('d', 4)), (1, 4))
   assert t is not u is not v


def test_difference_02( ):
   '''Partially intersecting chords;
      shared pitches removed from RHS.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([1, 2, 3], (1, 4))
   v = t - u
   assert isinstance(v, Note)
   assert v.signature == ((('c', 4), ), (1, 4))
   assert t is not u is not v


def test_difference_03( ):
   '''Wholly intersecting chords;
      all pitches removed and rest returns.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([0, 1, 2], (1, 4))
   v = t - u
   assert isinstance(v, Rest)
   assert v.signature == (( ), (1, 4))
   assert t is not u is not v
   

def test_difference_04( ):
   '''Enharmonically disjunct;
      enharmonic RHS equivalent appears;
      shared pitches disappear.'''
   t = Chord([0, ('cs', 4), 2], (1, 4))
   u = Chord([0, ('df', 4), 2], (1, 4))
   v = t - u
   assert isinstance(v, Note)
   assert v.signature == ((('cs', 4), ), (1, 4))
   assert t is not u is not v


def test_difference_05( ):
   '''Duration inequality;
      noncommutative operation takes duration from LHS.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([3, 4, 5], (1, 8))
   v = t - u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('cs', 4), ('d', 4)), (1, 4))
   assert v.duration.written == t.duration.written
   assert t is not u is not v


def test_difference_06( ):
   '''Duration inequality;
      noncommutative operation takes duration from LHS.'''
   t = Chord([0, 1, 2], (1, 8))
   u = Chord([3, 4, 5], (1, 4))
   v = t - u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('cs', 4), ('d', 4)), (1, 8))
   assert v.duration.written == t.duration.written
   assert t is not u is not v


def test_difference_07( ):
   '''Rest from from produces rest.'''
   t = Rest((1, 4))
   u = Rest((1, 4))
   v = t - u
   assert isinstance(v, Rest)
   assert v.signature == (( ), (1, 4))
   assert t is not u is not v


def test_difference_08( ):
   '''Note from rest produces rest.'''
   t = Rest((1, 4))
   u = Note(0, (1, 4))
   v = t - u
   assert isinstance(v, Rest)
   assert v.signature == (( ), (1, 4))
   assert t is not u is not v


def test_difference_09( ):
   '''Note from like pitched note produces rest.'''
   t = Note(0, (1, 4))
   u = Note(0, (1, 4))
   v = t - u
   assert isinstance(v, Rest)
   assert v.signature == (( ), (1, 4))
   assert t is not u is not v


def test_difference_10( ):
   '''Note from differently pitched note produces note.'''
   t = Note(0, (1, 4))
   u = Note(2, (1, 4))
   v = t - u
   assert isinstance(v, Note)
   assert v.signature == ((('c', 4), ), (1, 4))
   assert t is not u is not v


def test_difference_11( ):
   '''Differently pitched note from chord
      produces chord.'''
   t = Chord([0, 2], (1, 4))
   u = Note(4, (1, 4))
   v = t - u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('d', 4)), (1, 4))
   assert t is not u is not v


def test_difference_12( ):
   '''Like pitched note from chord
      removes pitch.'''
   t = Chord([0, 2], (1, 4))
   u = Note(0, (1, 4))
   v = t - u
   assert isinstance(v, Note)
   assert v.signature == ((('d', 4), ), (1, 4))
   assert t is not u is not v
