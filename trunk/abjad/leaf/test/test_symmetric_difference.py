from abjad import *


### TODO: decide what happens when one or the other chord is *spanned*;
###       then write some tests to lock in that behavior.

def test_symmetric_difference_01( ):
   '''Chords completely disjunct;
      all pitches preserved.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([3, 4, 5], (1, 4))
   v = t ^ u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('cs', 4), ('d', 4), ('ef', 4), ('e', 4), ('f', 4)), (1, 4))
   assert t is not u is not v


def test_symmetric_difference_02( ):
   '''Partially intersecting chords;
      shared pitches do not appear at all.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([1, 2, 3], (1, 4))
   v = t ^ u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('ef', 4)), (1, 4))
   assert t is not u is not v


def test_symmetric_difference_03( ):
   '''Wholly intersecting chords;
      returns no pitches at all.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([0, 1, 2], (1, 4))
   v = t ^ u
   assert isinstance(v, Skip)
   assert v.signature == (( ), (1, 4))
   assert t is not u is not v
   

def test_symmetric_difference_04( ):
   '''Enharmonically disjunct;
      enharmonic equivalents both appear.'''
   t = Chord([0, ('cs', 4), 2], (1, 4))
   u = Chord([0, ('df', 4), 2], (1, 4))
   v = t ^ u
   assert isinstance(v, Chord)
   assert v.signature == ((('cs', 4), ('df', 4)), (1, 4))
   assert t is not u is not v


def test_symmetric_difference_05( ):
   '''Duration inequality;
      noncommutative operation takes duration from LHS.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([3, 4, 5], (1, 8))
   v = t ^ u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('cs', 4), ('d', 4), ('ef', 4), ('e', 4), ('f', 4)), (1, 4))
   assert v.duration.written.pair == t.duration.written.pair
   assert t is not u is not v


def test_symmetric_difference_06( ):
   '''Duration inequality;
      noncommutative operation takes duration from LHS.'''
   t = Chord([0, 1, 2], (1, 8))
   u = Chord([3, 4, 5], (1, 4))
   v = t ^ u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('cs', 4), ('d', 4), ('ef', 4), ('e', 4), ('f', 4)), (1, 8))
   assert v.duration.written.pair == t.duration.written.pair
   assert t is not u is not v


def test_symmetric_difference_07( ):
   '''Skip in symmetric difference with skip produces skip.'''
   t = Skip((1, 4))
   u = Skip((1, 4))
   v = t ^ u
   assert isinstance(v, Skip)
   assert v.signature == (( ), (1, 4))
   assert t is not u is not v


def test_symmetric_difference_08( ):
   '''Skip in symmetric difference with note produces note.'''
   t = Skip((1, 4))
   u = Note(0, (1, 4))
   v = t ^ u
   assert isinstance(v, Note)
   assert v.signature == ((('c', 4), ), (1, 4))
   assert t is not u is not v


def test_symmetric_difference_09( ):
   '''Note in symmetric difference with like 
      pitched note produces skip.'''
   t = Note(0, (1, 4))
   u = Note(0, (1, 4))
   v = t ^ u
   assert isinstance(v, Skip)
   assert v.signature == (( ), (1, 4))
   assert t is not u is not v


def test_symmetric_difference_10( ):
   '''Note in symmetric difference with differently pitched note
      produces chord.'''
   t = Note(0, (1, 4))
   u = Note(2, (1, 4))
   v = t ^ u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('d', 4)), (1, 4))
   assert t is not u is not v


def test_symmetric_difference_11( ):
   '''Chord in symmetric difference with differently 
      pitched note produces chord.'''
   t = Chord([0, 2], (1, 4))
   u = Note(4, (1, 4))
   v = t ^ u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('d', 4), ('e', 4)), (1, 4))
   assert t is not u is not v


def test_symmetric_difference_12( ):
   '''Chord in symmetric difference with like 
      pitched note removes shared note.'''
   t = Chord([0, 2], (1, 4))
   u = Note(0, (1, 4))
   v = t ^ u
   assert isinstance(v, Note)
   assert v.signature == ((('d', 4), ), (1, 4))
   assert t is not u is not v
