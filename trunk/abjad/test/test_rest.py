from abjad import *


### TEST TYPICAL REST ###

def test_typical_rest_01( ):
   r = Rest((1, 4))
   assert repr(r) == 'Rest(4)'
   assert r.format == 'r4'
   assert r.duration == r.duratum == Duration(1, 4)


### TEST CAST REST AS NOTE ###

def test_cast_rest_as_note_01( ):
   r = Rest((1, 8))
   d = r.duration
   r = Note(r)
   assert isinstance(r, Note)
   assert r._parent is None
   assert r.duration == d


def test_cast_rest_as_note_02( ):
   t = FixedDurationTuplet((2, 8), Rest((1, 8)) * 3)
   d = t[0].duration
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0]._parent is t
   assert t[0].duration == d


def test_cast_rest_as_note_03( ):
   v = Voice(Rest((1, 8)) * 3)
   d = v[0].duration
   Note(v[0])
   assert isinstance(v[0], Note)
   assert v[0]._parent is v
   assert v[0].duration == d


def test_cast_rest_as_note_04( ):
   t = Staff(Rest((1, 8)) * 3)
   d = t[0].duration
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0]._parent is t
   assert t[0].duration == d


### TEST CAST REST AS CHORD ###

def test_cast_rest_as_chord_01( ):
   r = Rest((1, 8))
   d = r.duration
   r = Chord(r)
   assert isinstance(r, Chord)
   assert r._parent is None
   assert r.duration == d


def test_cast_rest_as_chord_02( ):
   t = FixedDurationTuplet((2, 8), Rest((1, 8)) * 3)
   d = t[0].duration
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0]._parent is t
   assert t[0].duration == d


def test_cast_rest_as_chord_03( ):
   v = Voice(Rest((1, 8)) * 3)
   d = v[0].duration
   Chord(v[0])
   assert isinstance(v[0], Chord)
   assert v[0]._parent is v
   assert v[0].duration == d


def test_cast_rest_as_chord_04( ):
   t = Staff(Rest((1, 8)) * 3)
   d = t[0].duration
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0]._parent is t
   assert t[0].duration == d


### TEST CAST REST AS SKIP ###

def test_cast_rest_as_skip_01( ):
   r = Rest((1, 8))
   d = r.duration
   r = Skip(r)
   assert isinstance(r, Skip)
   assert r._parent is None
   assert r.duration == d


def test_cast_rest_as_skip_02( ):
   t = FixedDurationTuplet((2, 8), Rest((1, 8)) * 3)
   d = t[0].duration
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0]._parent is t
   assert t[0].duration == d


def test_cast_rest_as_skip_03( ):
   v = Voice(Rest((1, 8)) * 3)
   d = v[0].duration
   Skip(v[0])
   assert isinstance(v[0], Skip)
   assert v[0]._parent is v
   assert v[0].duration == d


def test_cast_rest_as_skip_04( ):
   t = Staff(Rest((1, 8)) * 3)
   d = t[0].duration
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0]._parent is t
   assert t[0].duration == d
