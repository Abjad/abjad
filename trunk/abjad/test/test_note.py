from abjad import *
from py.test import raises


### TEST REWRITE DURATION AS ###

def test_rewrite_duration_as_01a( ):
   n = Note(0, (1, 4))
   n.duration.rewrite((3, 16))
   assert n.duration.written == Rational(3, 16)
   assert n.duration.multiplier == Rational(4, 3)
   assert n.duration.absolute == Rational(1, 4)


def test_rewrite_duration_as_01b( ):
   n = Note(0, (1, 4))
   n.duration.rewrite(Rational(3, 16))
   assert n.duration.written == Rational(3, 16)
   assert n.duration.multiplier == Rational(4, 3)
   assert n.duration.absolute == Rational(1, 4)


def test_rewrite_duration_as_01c( ):
   n = Note(0, (1, 4))
   n.duration.rewrite(Rational(3, 16))
   assert n.duration.written == Rational(3, 16)
   assert n.duration.multiplier == Rational(4, 3)
   assert n.duration.absolute == Rational(1, 4)


def test_rewrite_duration_as_02( ):
   n = Note(0, (1, 4))
   n.duration.rewrite((3, 16))
   assert n.duration.written == Rational(3, 16)
   assert n.duration.multiplier == Rational(4, 3)
   assert n.duration.absolute == Rational(1, 4)


def test_rewrite_duration_as_03( ):
   n = Note(0, (1, 4))
   n.duration.rewrite((7, 8))
   assert n.duration.written == Rational(7, 8)
   assert n.duration.multiplier == Rational(2, 7)
   assert n.duration.absolute == Rational(1, 4)


def test_rewrite_duration_as_04( ):
   n = Note(0, (1, 4))
   n.duration.rewrite((15, 16))
   assert n.duration.written == Rational(15, 16)
   assert n.duration.multiplier == Rational(4, 15)
   assert n.duration.absolute == Rational(1, 4)


### TEST CAST NOTE AS REST ###

def test_cast_note_as_rest_01( ):
   n = Note(2, (1, 8))
   d = n.duration.written
   r = Rest(n)
   assert isinstance(r, Rest)
   # check that attributes have not been removed or added.
   assert dir(n) == dir(Note(0, (1, 8)))
   assert dir(r) == dir(Rest((1, 4)))
   assert r.format == 'r8'
   assert r._parent is None
   assert r.duration.written == d


def test_cast_note_as_rest_02( ):
   t = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   d = t[0].duration.written
   Rest(t[0])
   assert t[0].format == 'r8'
   assert isinstance(t[0], Rest)
   assert t[0]._parent is t
   assert t[0].duration.written == d


def test_cast_note_as_rest_03( ):
   v = Voice(Note(0, (1, 8)) * 3)
   d = v[0].duration.written
   Rest(v[0])
   assert v[0].format == 'r8'
   assert isinstance(v[0], Rest)
   assert v[0]._parent is v
   assert v[0].duration.written == d


def test_cast_note_as_rest_04( ):
   t = Staff(Note(0, (1, 8)) * 3)
   d = t[0].duration.written
   Rest(t[0])
   assert t[0].format == 'r8'
   assert isinstance(t[0], Rest)
   assert t[0]._parent is t
   assert t[0].duration.written == d


### TEST CAST NOTE AS CHORD ###

def test_cast_note_as_chord_01( ):
   n = Note(2, (1, 8))
   h, p, d = n.notehead, n.pitch, n.duration.written
   c = Chord(n)
   assert isinstance(c, Chord)
   # check that attributes have not been removed or added.
   assert dir(n) == dir(Note(0, (1, 4)))
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert c.format == "<d'>8"
   assert c._parent is None
   assert c.noteheads[0] is not h
   assert c.pitches[0].number == p.number
   assert c.duration.written == d


def test_cast_note_as_chord_02( ):
   t = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   h, p, d = t[0].notehead, t[0].pitch, t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0].format == "<c'>8"
   assert t[0]._parent is t
   assert t[0].noteheads[0] is not h
   assert t[0].pitches[0].number == p.number
   assert t[0].duration.written == d


def test_cast_note_as_chord_03( ):
   v = Voice(Note(0, (1, 8)) * 3)
   h, p, d = v[0].notehead, v[0].pitch, v[0].duration.written
   Chord(v[0])
   assert isinstance(v[0], Chord)
   assert v[0].format == "<c'>8"
   assert v[0]._parent is v
   assert v[0].noteheads[0] is not h
   assert v[0].pitches[0].number == p.number
   assert v[0].duration.written == d


def test_cast_note_as_chord_04( ):
   t = Staff(Note(0, (1, 8)) * 3)
   h, p, d = t[0].notehead, t[0].pitch, t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0].format == "<c'>8"
   assert t[0]._parent is t
   assert t[0].noteheads[0] is not h
   assert t[0].pitches[0].number == p.number
   assert t[0].duration.written == d


### TEST CAST NOTE AS SKIP ###

def test_cast_note_as_skip_01( ):
   n = Note(2, (1, 8))
   d = n.duration.written
   s = Skip(n)
   assert isinstance(s, Skip)
   # check that attributes have not been removed or added.
   assert dir(n) == dir(Note(0, (1, 4)))
   assert dir(s) == dir(Skip((1, 4)))
   assert s.format == 's8'
   assert s._parent is None
   assert s.duration.written == d


def test_cast_note_as_skip_02( ):
   t = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   d = t[0].duration.written
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0].format == 's8'
   assert t[0]._parent is t
   assert t[0].duration.written == d


def test_cast_note_as_skip_03( ):
   v = Voice(Note(0, (1, 8)) * 3)
   d = v[0].duration.written
   Skip(v[0])
   assert isinstance(v[0], Skip)
   assert v[0].format == 's8'
   assert v[0]._parent is v
   assert v[0].duration.written == d


def test_cast_note_as_skip_04( ):
   t = Staff(Note(0, (1, 8)) * 3)
   d = t[0].duration.written
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0].format == 's8'
   assert t[0]._parent is t
   assert t[0].duration.written == d


### TEST OCTAVE ZERO ###

def test_octave_zero_01( ):
   '''Notes print correctly when pitch is in octave 0.'''
   t = Note(-37, (1, 4))
   assert t.format == 'b,,,4'


### ASSERTS ###

def test_assert_duration_is_notehead_assignable_01( ):
   raises(ValueError, Note, 0, (5, 8))
