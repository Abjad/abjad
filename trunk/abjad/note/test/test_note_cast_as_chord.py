from abjad import *
from py.test import raises


def test_cast_chord_01( ):
   n = Note(2, (1, 8))
   h, p, d = n.notehead, n.pitch, n.duration.written
   c = Chord(n)
   assert isinstance(c, Chord)
   # check that attributes have not been removed or added.
   assert dir(n) == dir(Note(0, (1, 4)))
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert c.format == "<d'>8"
   assert c.parentage.parent is None
   assert c.noteheads[0] is not h
   assert c.pitches[0].number == p.number
   assert c.duration.written == d


def test_cast_chord_02( ):
   t = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   h, p, d = t[0].notehead, t[0].pitch, t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0].format == "<c'>8"
   assert t[0].parentage.parent is t
   assert t[0].noteheads[0] is not h
   assert t[0].pitches[0].number == p.number
   assert t[0].duration.written == d


def test_cast_chord_03( ):
   v = Voice(Note(0, (1, 8)) * 3)
   h, p, d = v[0].notehead, v[0].pitch, v[0].duration.written
   Chord(v[0])
   assert isinstance(v[0], Chord)
   assert v[0].format == "<c'>8"
   assert v[0].parentage.parent is v
   assert v[0].noteheads[0] is not h
   assert v[0].pitches[0].number == p.number
   assert v[0].duration.written == d


def test_cast_chord_04( ):
   t = Staff(Note(0, (1, 8)) * 3)
   h, p, d = t[0].notehead, t[0].pitch, t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0].format == "<c'>8"
   assert t[0].parentage.parent is t
   assert t[0].noteheads[0] is not h
   assert t[0].pitches[0].number == p.number
   assert t[0].duration.written == d


def test_cast_chord_05( ):
   '''Works fine when note is beamed.'''
   t = Staff(Note(0, (1, 8)) * 3)
   Beam(t[ : ])
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0].parentage.parent is t
