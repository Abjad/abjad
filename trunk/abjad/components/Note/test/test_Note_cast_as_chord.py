from abjad import *
from py.test import raises
import py
py.test.skip('make casting work again before removing casting permanently.')


def test_Note_cast_as_chord_01( ):
   n = Note(2, (1, 8))
   h, p, d = n.note_head, n.pitch, n.duration.written
   c = Chord(n)
   assert isinstance(c, Chord)
   # check that attributes have not been removed or added.
   assert dir(n) == dir(Note(0, (1, 4)))
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert c.format == "<d'>8"
   assert c._parentage.parent is None
   assert c.note_heads[0] is not h
   assert c.pitches[0].number == p.number
   assert c.duration.written == d


def test_Note_cast_as_chord_02( ):
   t = tuplettools.FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   h, p, d = t[0].note_head, t[0].pitch, t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0].format == "<c'>8"
   assert t[0]._parentage.parent is t
   assert t[0].note_heads[0] is not h
   assert t[0].pitches[0].number == p.number
   assert t[0].duration.written == d


def test_Note_cast_as_chord_03( ):
   v = Voice(Note(0, (1, 8)) * 3)
   h, p, d = v[0].note_head, v[0].pitch, v[0].duration.written
   Chord(v[0])
   assert isinstance(v[0], Chord)
   assert v[0].format == "<c'>8"
   assert v[0]._parentage.parent is v
   assert v[0].note_heads[0] is not h
   assert v[0].pitches[0].number == p.number
   assert v[0].duration.written == d


def test_Note_cast_as_chord_04( ):
   t = Staff(Note(0, (1, 8)) * 3)
   h, p, d = t[0].note_head, t[0].pitch, t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0].format == "<c'>8"
   assert t[0]._parentage.parent is t
   assert t[0].note_heads[0] is not h
   assert t[0].pitches[0].number == p.number
   assert t[0].duration.written == d


def test_Note_cast_as_chord_05( ):
   '''Works fine when note is beamed.'''
   t = Staff(Note(0, (1, 8)) * 3)
   spannertools.BeamSpanner(t[:])
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0]._parentage.parent is t
