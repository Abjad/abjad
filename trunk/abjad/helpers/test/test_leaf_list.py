from abjad import *


def test_leaf_list_01( ):
   '''Works on note instances;
      returns notes with no pitch.'''
   leaves = leaf_list(Note(0, (1, 4)), (9, 16))
   assert all([isinstance(leaf, Note) for leaf in leaves])
   assert leaves[0].duration.written == Rational(1, 2)
   assert leaves[1].duration.written == Rational(1, 16)
   '''[Note(c', 2), Note(c', 16)]'''


def test_leaf_list_02( ):
   '''Works on rest instances.'''
   leaves = leaf_list(Rest((1, 4)), (9, 16))
   assert all([isinstance(leaf, Rest) for leaf in leaves])
   assert leaves[0].duration.written == Rational(1, 2)
   assert leaves[1].duration.written == Rational(1, 16)
   '''[Rest(2), Rest(16)]'''


def test_leaf_list_03( ):
   '''Works on chord instances.'''
   leaves = leaf_list(Chord([2, 3, 4], (1, 4)), (9, 16))
   assert all([isinstance(leaf, Chord) for leaf in leaves])
   assert leaves[0].duration.written == Rational(1, 2)
   assert leaves[1].duration.written == Rational(1, 16)
   '''[Chord(d' ef' e', 2), Chord(d' ef' e', 16)]'''


def test_leaf_list_04( ):
   '''Works on skip instances.'''
   leaves = leaf_list(Skip((1, 4)), (9, 16))
   assert all([isinstance(leaf, Skip) for leaf in leaves])
   assert leaves[0].duration.written == Rational(1, 2)
   assert leaves[1].duration.written == Rational(1, 16)
   '''[Skip(2), Skip(16)]'''


def test_leaf_list_05( ):
   '''Works on Note type;
      returns notes with None pitch.'''
   leaves = leaf_list(Note, (9, 16))
   assert all([isinstance(leaf, Note) for leaf in leaves])
   assert leaves[0].duration.written == Rational(1, 2)
   assert leaves[1].duration.written == Rational(1, 16)
   '''[Note(None, 2), Note(None, 16)]'''


def test_leaf_list_06( ):
   '''Works on Rest type.'''
   leaves = leaf_list(Rest, (9, 16))
   assert all([isinstance(leaf, Rest) for leaf in leaves])
   assert leaves[0].duration.written == Rational(1, 2)
   assert leaves[1].duration.written == Rational(1, 16)
   '''[Rest(2), Rest(16)]'''


def test_leaf_list_07( ):
   '''Works on Chord type;
      returns chords with empty pitch list.'''
   leaves = leaf_list(Chord, (9, 16))
   assert all([isinstance(leaf, Chord) for leaf in leaves])
   assert leaves[0].duration.written == Rational(1, 2)
   assert leaves[1].duration.written == Rational(1, 16)
   '''[Chord(, 2), Chord(, 16)]''' 


def test_leaf_list_08( ):
   '''Works on Skip type.'''
   leaves = leaf_list(Skip, (9, 16))
   assert all([isinstance(leaf, Skip) for leaf in leaves])
   assert leaves[0].duration.written == Rational(1, 2)
   assert leaves[1].duration.written == Rational(1, 16)
   '''[Skip(2), Skip(16)]'''
