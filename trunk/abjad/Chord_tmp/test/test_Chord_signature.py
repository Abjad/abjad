from abjad import *


def test_Chord_signature_01( ):
   '''Chord signature is a pair comprising pitch pairs tuple
      together with written duration pair.'''
   t = Chord([2, 4, 5], (1, 4))
   assert t.signature == ((('d', 4), ('e', 4), ('f', 4)), (1, 4))


def test_Chord_signature_02( ):
   '''Chords with like pitch content and written duration
      carry the same signature.'''
   t1 = Chord([2, 4, 5], (1, 4))
   t2 = Chord([2, 4, 5], (1, 4))
   assert t1.signature == t2.signature


def test_Chord_signature_03( ):
   '''Chords with different pitch content carry different signatures.'''
   t1 = Chord([2, 4, 5], (1, 4))
   t2 = Chord([6, 7, 10], (1, 4))
   assert not t1.signature == t2.signature


def test_Chord_signature_04( ):
   '''Chords with different written duration carry different signatures.'''
   t1 = Chord([2, 4, 5], (1, 4))
   t2 = Chord([2, 4, 5], (1, 8))
   assert not t1.signature == t2.signature


def test_Chord_signature_05( ):
   '''Empty chords carry a signature with empty pitch pairs tuple.'''
   t1 = Chord([ ], (1, 4))
   assert t1.signature == (( ), (1, 4))


def test_Chord_signature_06( ):
   '''Emtpy chords with like written duration carry 
      the same signature.'''
   t1 = Chord([ ], (1, 4))
   t2 = Chord([ ], (1, 4))
   assert t1.signature == t2.signature
