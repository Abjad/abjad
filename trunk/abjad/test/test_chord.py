from abjad import *
from py.test import raises


### TEST DEMO PUBLIC CHORD INTERFACE ###

def test_demo_public_chord_interface_01( ):
   t = Chord([2, 3, 4], (1, 4))
   assert repr(t) == "Chord(d' ef' e', 4)"
   assert str(t) == "<d' ef' e'>4"
   assert t.format == "<d' ef' e'>4"
   assert len(t) == 3
   assert len(t.noteheads) == 3
   assert len(t.pitches) == 3
   assert t.duration == t.duration.prolated == Rational(1, 4)


### TEST TWEAKED CHORD ###

def test_tweaked_chord_01( ):
   t = Chord([2, 3, 4], (1, 4))
   t[0].style = 'harmonic'
   assert t.format == "<\n\t\\tweak #'style #'harmonic\n\td'\n\tef'\n\te'\n>4"

def test_tweaked_chord_02( ):
   t = Chord([2, 3, 4], (1, 4))
   t[0].transparent = True
   assert t.format == "<\n\t\\tweak #'transparent ##t\n\td'\n\tef'\n\te'\n>4"


### TEST ONE-NOTE CHORD ###
### the point here is that one-note chords ###
### format as chords and not as single notes ###

def test_one_note_chord_01( ):
   t = Chord([0], (1, 4))
   assert repr(t) == "Chord(c', 4)"
   assert str(t) == "<c'>4"
   assert t.format == "<c'>4"
   assert len(t) == 1
   assert len(t.noteheads) == 1
   assert len(t.pitches) == 1

def test_one_note_chord_02( ):
   t = Chord([0.5], (1, 4))
   assert repr(t) == "Chord(cqs', 4)"
   assert str(t) == "<cqs'>4"
   assert t.format == "<cqs'>4"
   assert len(t) == 1
   assert len(t.noteheads) == 1
   assert len(t.pitches) == 1


### TEST CAST CHORD AS NOTE ###

def test_cast_chord_as_note_01( ):
   c = Chord([2, 3, 4], (1, 4))
   duration = c.duration.written
   n = Note(c)
   assert isinstance(n, Note)
   # check that attributes have not been removed or added.
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert dir(n) == dir(Note(0, (1, 4)))
   assert n._parent is None
   assert n.duration == duration

def test_cast_chord_as_note_02( ):
   t = FixedDurationTuplet((2, 8), Chord([2, 3, 4], (1, 4)) * 3)
   d = t[0].duration.written
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0]._parent is t
   assert t[0].duration == d

def test_cast_chord_as_note_03( ):
   v = Voice(Chord([2, 3, 4], (1, 4)) * 3)
   d = v[0].duration.written
   Note(v[0])
   assert isinstance(v[0], Note)
   assert v[0]._parent is v
   assert v[0].duration == d

def test_cast_chord_as_note_04( ):
   t = Staff(Chord([2, 3, 4], (1, 4)) * 3)
   d = t[0].duration.written
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0]._parent is t
   assert t[0].duration == d


### TEST CAST CHORD AS REST ###

def test_cast_chord_as_rest_01( ):
   c = Chord([2, 3, 4], (1, 4))
   duration = c.duration.written
   r = Rest(c)
   assert isinstance(r, Rest)
   # check that attributes have not been removed or added.
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert dir(r) == dir(Rest((1, 4)))
   assert r._parent is None
   assert r.duration == duration

def test_cast_chord_as_rest_02( ):
   t = FixedDurationTuplet((2, 8), Chord([2, 3, 4], (1, 4)) * 3)
   d = t[0].duration.written
   Rest(t[0])
   assert isinstance(t[0], Rest)
   assert t[0]._parent is t
   assert t[0].duration == d

def test_cast_chord_as_rest_03( ):
   v = Voice(Chord([2, 3, 4], (1, 4)) * 3)
   d = v[0].duration.written
   Rest(v[0])
   assert isinstance(v[0], Rest)
   assert v[0]._parent is v
   assert v[0].duration == d

def test_cast_chord_as_rest_04( ):
   t = Staff(Chord([2, 3, 4], (1, 4)) * 3)
   d = t[0].duration.written
   Rest(t[0])
   assert isinstance(t[0], Rest)
   assert t[0]._parent is t
   assert t[0].duration == d


### TEST CAST CHORD AS SKIP ###

def test_cast_chord_as_skip_01( ):
   c = Chord([2, 3, 4], (1, 4))
   duration = c.duration.written
   s = Skip(c)
   assert isinstance(s, Skip)
   # check that attributes have not been removed or added.
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert dir(s) == dir(Skip((1, 4)))
   assert s._parent is None
   assert s.duration == duration

def test_cast_chord_as_skip_02( ):
   t = FixedDurationTuplet((2, 8), Chord([2, 3, 4], (1, 4)) * 3)
   d = t[0].duration.written
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0]._parent is t
   assert t[0].duration == d

def test_cast_chord_as_skip_03( ):
   v = Voice(Chord([2, 3, 4], (1, 4)) * 3)
   d = v[0].duration.written
   Skip(v[0])
   assert isinstance(v[0], Skip)
   assert v[0]._parent is v
   assert v[0].duration == d

def test_cast_chord_as_skip_04( ):
   t = Staff(Chord([2, 3, 4], (1, 4)) * 3)
   d = t[0].duration.written
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0]._parent is t
   assert t[0].duration == d


### TEST CHORD FORMAT RIGHT ###

def test_chord_format_right_01( ):
   '''Untweaked chords format right.'''
   t = Chord([2, 3, 4], (1, 4))
   t.glissando = True
   assert t.format == "<d' ef' e'>4 \\glissando"
   '''
   <d' ef' e'>4 \glissando
   '''


def test_chord_format_right_02( ):
   '''Untweaked chords format right.'''
   t = Chord([2, 3, 4], (1, 4))
   t[0].color = 'red'
   t.glissando = True
   assert t.format == "<\n\t\\tweak #'color #red\n\td'\n\tef'\n\te'\n>4 \\glissando"
   '''
   <
           \tweak #'color #red
           d'
           ef'
           e'
   >4 \glissando
   '''
