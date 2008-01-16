from abjad import *


### TEST DEMO SKIP PUBLIC INTERFACE ###

def test_demo_skip_public_interface_01( ):
   s = Skip((1, 8))
   assert repr(s) == 'Skip(8)'
   assert str(s) == 's8'
   assert s.format == 's8'
   assert s.duration == s.duratum == Duration(1, 8)

def test_demo_skip_public_interface_02( ):
   s = Skip((3, 16))
   assert repr(s) == 'Skip(8.)'
   assert str(s) == 's8.'
   assert s.format == 's8.'
   assert s.duration == s.duratum == Duration(3, 16)


### TEST CAST SKIP AS NOTE ###

def test_cast_skip_as_note_01( ):
   s = Skip((1, 8))
   d = s.duration
   s = s.caster.toNote( )
   assert isinstance(s, Note)
   assert s._parent is None
   assert s.duration == d

def test_cast_skip_as_note_02( ):
   t = FixedDurationTuplet((2, 8), Skip((1, 8)) * 3)
   d = t[0].duration
   t[0].caster.toNote( )
   assert isinstance(t[0], Note)
   assert t[0]._parent is t
   assert t[0].duration == d

def test_cast_skip_as_note_03( ):
   v = Voice(Skip((1, 8)) * 3)
   d = v[0].duration
   v[0].caster.toNote( )
   assert isinstance(v[0], Note)
   assert v[0]._parent is v
   assert v[0].duration == d

def test_cast_skip_as_note_04( ):
   t = Staff(Skip((1, 8)) * 3)
   d = t[0].duration
   t[0].caster.toNote( )
   assert isinstance(t[0], Note)
   assert t[0]._parent is t
   assert t[0].duration == d


### TEST CAST SKIP AS REST ###

def test_cast_skip_as_rest_01( ):
   s = Skip((1, 8))
   d = s.duration
   s = s.caster.toRest( )
   assert isinstance(s, Rest)
   assert s._parent is None
   assert s.duration == d

def test_cast_skip_as_rest_02( ):
   t = FixedDurationTuplet((2, 8), Skip((1, 8)) * 3)
   d = t[0].duration
   t[0].caster.toRest( )
   assert isinstance(t[0], Rest)
   assert t[0]._parent is t
   assert t[0].duration == d

def test_cast_skip_as_rest_03( ):
   v = Voice(Skip((1, 8)) * 3)
   d = v[0].duration
   v[0].caster.toRest( )
   assert isinstance(v[0], Rest)
   assert v[0]._parent is v
   assert v[0].duration == d

def test_cast_skip_as_rest_04( ):
   t = Staff(Skip((1, 8)) * 3)
   d = t[0].duration
   t[0].caster.toRest( )
   assert isinstance(t[0], Rest)
   assert t[0]._parent is t
   assert t[0].duration == d


### TEST CAST REST AS CHORD ###

def test_cast_skip_as_chord_01( ):
   s = Skip((1, 8))
   d = s.duration
   s = s.caster.toChord( )
   assert isinstance(s, Chord)
   assert s._parent is None
   assert s.duration == d

def test_cast_skip_as_chord_02( ):
   t = FixedDurationTuplet((2, 8), Skip((1, 8)) * 3)
   d = t[0].duration
   t[0].caster.toChord( )
   assert isinstance(t[0], Chord)
   assert t[0]._parent is t
   assert t[0].duration == d

def test_cast_skip_as_chord_03( ):
   v = Voice(Skip((1, 8)) * 3)
   d = v[0].duration
   v[0].caster.toChord( )
   assert isinstance(v[0], Chord)
   assert v[0]._parent is v
   assert v[0].duration == d

def test_cast_skip_as_chord_04( ):
   t = Staff(Skip((1, 8)) * 3)
   d = t[0].duration
   t[0].caster.toChord( )
   assert isinstance(t[0], Chord)
   assert t[0]._parent is t
   assert t[0].duration == d
