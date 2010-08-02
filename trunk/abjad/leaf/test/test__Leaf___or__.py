from abjad import *


def test_leaf_union_01( ):
   '''Chords completely disjunct;
      all pitches preserved.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([3, 4, 5], (1, 4))
   v = t | u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('cs', 4), ('d', 4), ('ef', 4), ('e', 4), ('f', 4)), (1, 4))
   assert t is not u is not v


def test_leaf_union_02( ):
   '''Partially intersecting chords;
      shared pitches appear only once.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([1, 2, 3], (1, 4))
   v = t | u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('cs', 4), ('d', 4), ('ef', 4)), (1, 4))
   assert t is not u is not v


def test_leaf_union_03( ):
   '''Wholly intersecting chords;
      shared pitches appear only once.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([0, 1, 2], (1, 4))
   v = t | u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('cs', 4), ('d', 4)), (1, 4))
   assert t is not u is not v
   

def test_leaf_union_04( ):
   '''Enharmonically disjunct;
      enharmonic equivalents both appear.'''
   t = Chord([0, ('cs', 4), 2], (1, 4))
   u = Chord([0, ('df', 4), 2], (1, 4))
   v = t | u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('cs', 4), ('df', 4), ('d', 4)), (1, 4))
   assert t is not u is not v


def test_leaf_union_05( ):
   '''Duration inequality;
      noncommutative union takes from LHS.'''
   t = Chord([0, 1, 2], (1, 4))
   u = Chord([3, 4, 5], (1, 8))
   v = t | u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('cs', 4), ('d', 4), ('ef', 4), ('e', 4), ('f', 4)), (1, 4))
   assert v.duration.written == t.duration.written
   assert t is not u is not v


def test_leaf_union_06( ):
   '''Duration inequality;
      noncommutative union takes from LHS.'''
   t = Chord([0, 1, 2], (1, 8))
   u = Chord([3, 4, 5], (1, 4))
   v = t | u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('cs', 4), ('d', 4), ('ef', 4), ('e', 4), ('f', 4)), (1, 8))
   assert v.duration.written == t.duration.written
   assert t is not u is not v


def test_leaf_union_07( ):
   '''Rest in union with rest produces rest.'''
   t = Rest((1, 4))
   u = Rest((1, 4))
   v = t | u
   assert isinstance(v, Rest)
   assert v.signature == (( ), (1, 4))
   assert t is not u is not v


def test_leaf_union_08( ):
   '''Rest in union with note produces note.'''
   t = Rest((1, 4))
   u = Note(0, (1, 4))
   v = t | u
   assert isinstance(v, Note)
   assert v.signature == ((('c', 4), ), (1, 4))
   assert t is not u is not v


def test_leaf_union_09( ):
   '''Note in union with like pitched note produces note.'''
   t = Note(0, (1, 4))
   u = Note(0, (1, 4))
   v = t | u
   assert isinstance(v, Note)
   assert v.signature == ((('c', 4), ), (1, 4))
   assert t is not u is not v


def test_leaf_union_10( ):
   '''Note in union with differently pitched note
      produces chord.'''
   t = Note(0, (1, 4))
   u = Note(2, (1, 4))
   v = t | u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('d', 4)), (1, 4))
   assert t is not u is not v


def test_leaf_union_11( ):
   '''Chord in union with differently pitched note
      produces chord.'''
   t = Chord([0, 2], (1, 4))
   u = Note(4, (1, 4))
   v = t | u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('d', 4), ('e', 4)), (1, 4))
   assert t is not u is not v


def test_leaf_union_12( ):
   '''Chord in union with like pitched note
      produces chord.'''
   t = Chord([0, 2], (1, 4))
   u = Note(0, (1, 4))
   v = t | u
   assert isinstance(v, Chord)
   assert v.signature == ((('c', 4), ('d', 4)), (1, 4))
   assert t is not u is not v
