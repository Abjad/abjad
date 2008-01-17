from abjad import *
from py.test import raises


### TEST INIT TYPICAL NOTE ###

def test_init_typical_note( ):

   n = Note(13, (3, 16))
   assert repr(n) == "Note(cs'', 8.)"
   assert repr(n.notehead) == "NoteHead(cs'')"
   assert repr(n.pitch) == 'Pitch(cs, 5)'
   assert repr(n.duration) == 'Duration(3, 16)'


### TEST INIT EMPTY NOTE ###

def test_init_empty_note_then_check_notehead_and_pitch( ):

   n = Note( )
   assert repr(n) == 'Note( )'
   assert n.notehead == None
   assert n.pitch == None

def test_init_empty_note_then_check_duration( ):

   n = Note( )
   assert repr(n) == 'Note( )'
   assert n.duration == None
   assert n.multiplier == None
   assert n.duratum == None


### TEST INIT EMPTY NOTE, THEN SET DURATION ###

def test_init_empty_note_then_set_duration_01a( ):

   n = Note( )
   n.duration = (1, 4)
   assert repr(n) == 'Note(4)'
   assert n.duration == Duration(1, 4)
   assert n.multiplier == None
   assert n.duratum == Duration(1, 4)

def test_init_empty_note_then_set_duration_01b( ):

   n = Note( )
   n.duration = Duration(1, 4)
   assert repr(n) == 'Note(4)'
   assert n.duration == Duration(1, 4)
   assert n.multiplier == None
   assert n.duratum == Duration(1, 4)

def test_init_empty_note_then_set_duration_01c( ):

   n = Note( )
   n.duration = Rational(1, 4)
   assert repr(n) == 'Note(4)'
   assert n.duration == Duration(1, 4)
   assert n.multiplier == None
   assert n.duratum == Duration(1, 4)


### TEST INIT EMPTY NOTE, THEN SET MULTIPLIER ###

def test_init_empty_note_then_set_multiplier_01a( ):

   n = Note( )
   n.multiplier = (1, 2)
   assert repr(n) == 'Note(0 * 1/2)'
   assert n.duration == None
   assert n.multiplier == Rational(1, 2)
   assert n.duratum == None

def test_init_empty_note_then_set_multiplier_01b( ):

   n = Note( )
   n.multiplier = Duration(1, 2)
   assert repr(n) == 'Note(0 * 1/2)'
   assert n.duration == None
   assert n.multiplier == Rational(1, 2)
   assert n.duratum == None

def test_init_empty_note_then_set_multiplier_01c( ):

   n = Note( )
   n.multiplier = Rational(1, 2)
   assert repr(n) == 'Note(0 * 1/2)'
   assert n.duration == None
   assert n.multiplier == Rational(1, 2)
   assert n.duratum == None


### TEST INIT NOTE WITH DURATION & MULTIPLIER ONLY ###

def test_init_note_with_duration_and_multiplier_only_01( ):
   n = Note(None, (1, 4), (1, 2)) 
   assert repr(n) == 'Note(4 * 1/2)'
   assert n.duration == Duration(1, 4)
   assert n.multiplier == Rational(1, 2)
   assert n.duratum == Duration(1, 8)


def test_init_note_with_duration_and_multiplier_only_02( ):
   n = Note(None, (1, 4), (2, 3)) 
   assert repr(n) == 'Note(4 * 2/3)'
   assert n.duration == Duration(1, 4)
   assert n.multiplier == Rational(2, 3)
   assert n.duratum == Duration(1, 6)


def test_init_note_with_duration_and_multiplier_only_03( ):
   n = Note(None, (3, 64), (2, 3)) 
   assert repr(n) == 'Note(32. * 2/3)'
   assert n.duration == Duration(3, 64)
   assert n.multiplier == Rational(2, 3)
   assert n.duratum == Duration(1, 32)


def test_init_note_with_duration_and_multiplier_only_04( ):
   n = Note(None, (7, 128), (5, 6))
   assert repr(n) == 'Note(32.. * 5/6)'
   assert n.duration == Duration(7, 128)
   assert n.multiplier == Rational(5, 6)
   assert n.duratum == Duration(35, 768)


### TEST INIT EMPTY NOTE, THEN ADD PITCH ###

def test_init_empty_note_then_add_pitch_01a( ):
   n = Note( )
   n.pitch = 13
   assert repr(n) == "Note(cs'')"
   assert n.pitch == Pitch(13)


def test_init_empty_note_then_add_pitch_01b( ):
   n = Note( )
   n.pitch = Pitch(13)
   assert repr(n) == "Note(cs'')"
   assert n.pitch == Pitch(13)


def test_init_empty_note_then_add_pitch_01c( ):
   n = Note( )
   n.pitch = ('cs', 5)
   assert repr(n) == "Note(cs'')"
   assert n.pitch == Pitch(13)


def test_init_empty_note_then_add_pitch_01c( ):
   n = Note( )
   n.pitch = (13, 'c')
   assert repr(n) == "Note(cs'')"
   assert n.pitch == Pitch(13)


### TEST REWRITE DURATION AS ###

def test_rewrite_duration_as_01a( ):
   n = Note(0, (1, 4))
   n.rewriteDurationAs((3, 16))
   assert n.duration == Duration(3, 16)
   assert n.multiplier == Rational(4, 3)
   assert n.duratum == Duration(1, 4)


def test_rewrite_duration_as_01b( ):
   n = Note(0, (1, 4))
   n.rewriteDurationAs(Rational(3, 16))
   assert n.duration == Duration(3, 16)
   assert n.multiplier == Rational(4, 3)
   assert n.duratum == Duration(1, 4)


def test_rewrite_duration_as_01c( ):
   n = Note(0, (1, 4))
   n.rewriteDurationAs(Duration(3, 16))
   assert n.duration == Duration(3, 16)
   assert n.multiplier == Rational(4, 3)
   assert n.duratum == Duration(1, 4)


def test_rewrite_duration_as_02( ):
   n = Note(0, (1, 4))
   n.rewriteDurationAs((3, 16))
   assert n.duration == Duration(3, 16)
   assert n.multiplier == Rational(4, 3)
   assert n.duratum == Duration(1, 4)


def test_rewrite_duration_as_03( ):
   n = Note(0, (1, 4))
   n.rewriteDurationAs((7, 8))
   assert n.duration == Duration(7, 8)
   assert n.multiplier == Rational(2, 7)
   assert n.duratum == Duration(1, 4)


def test_rewrite_duration_as_04( ):
   n = Note(0, (1, 4))
   n.rewriteDurationAs((15, 16))
   assert n.duration == Duration(15, 16)
   assert n.multiplier == Rational(4, 15)
   assert n.duratum == Duration(1, 4)


### TEST CAST NOTE AS REST ###

def test_cast_note_as_rest_01( ):
   n = Note(2, (1, 8))
   d = n.duration
   n = Rest(n)
   assert isinstance(n, Rest)
   assert n.format == 'r8'
   assert n._parent is None
   assert n.duration == d


def test_cast_note_as_rest_02( ):
   t = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   d = t[0].duration
   Rest(t[0])
   assert t[0].format == 'r8'
   assert isinstance(t[0], Rest)
   assert t[0]._parent is t
   assert t[0].duration == d


def test_cast_note_as_rest_03( ):
   v = Voice(Note(0, (1, 8)) * 3)
   d = v[0].duration
   Rest(v[0])
   assert v[0].format == 'r8'
   assert isinstance(v[0], Rest)
   assert v[0]._parent is v
   assert v[0].duration == d


def test_cast_note_as_rest_04( ):
   t = Staff(Note(0, (1, 8)) * 3)
   d = t[0].duration
   Rest(t[0])
   assert t[0].format == 'r8'
   assert isinstance(t[0], Rest)
   assert t[0]._parent is t
   assert t[0].duration == d


### TEST CAST NOTE AS CHORD ###

def test_cast_note_as_chord_01( ):
   n = Note(2, (1, 8))
   h, p, d = n.notehead, n.pitch, n.duration
   n = Chord(n)
   assert isinstance(n, Chord)
   assert n.format == "<d'>8"
   assert n._parent is None
   assert n.noteheads[0] is not h
   assert n.pitches[0].number == p.number
   assert n.duration.pair == d.pair


def test_cast_note_as_chord_02( ):
   t = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   h, p, d = t[0].notehead, t[0].pitch, t[0].duration
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0].format == "<c'>8"
   assert t[0]._parent is t
   assert t[0].noteheads[0] is not h
   assert t[0].pitches[0].number == p.number
   assert t[0].duration.pair == d.pair


def test_cast_note_as_chord_03( ):
   v = Voice(Note(0, (1, 8)) * 3)
   h, p, d = v[0].notehead, v[0].pitch, v[0].duration
   Chord(v[0])
   assert isinstance(v[0], Chord)
   assert v[0].format == "<c'>8"
   assert v[0]._parent is v
   assert v[0].noteheads[0] is not h
   assert v[0].pitches[0].number == p.number
   assert v[0].duration.pair == d.pair


def test_cast_note_as_chord_04( ):
   t = Staff(Note(0, (1, 8)) * 3)
   h, p, d = t[0].notehead, t[0].pitch, t[0].duration
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0].format == "<c'>8"
   assert t[0]._parent is t
   assert t[0].noteheads[0] is not h
   assert t[0].pitches[0].number == p.number
   assert t[0].duration.pair == d.pair


### TEST CAST NOTE AS SKIP ###

def test_cast_note_as_skip_01( ):
   n = Note(2, (1, 8))
   d = n.duration
   n = Skip(n)
   assert isinstance(n, Skip)
   assert n.format == 's8'
   assert n._parent is None
   assert n.duration == d


def test_cast_note_as_skip_02( ):
   t = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   d = t[0].duration
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0].format == 's8'
   assert t[0]._parent is t
   assert t[0].duration == d


def test_cast_note_as_skip_03( ):
   v = Voice(Note(0, (1, 8)) * 3)
   d = v[0].duration
   Skip(v[0])
   assert isinstance(v[0], Skip)
   assert v[0].format == 's8'
   assert v[0]._parent is v
   assert v[0].duration == d


def test_cast_note_as_skip_04( ):
   t = Staff(Note(0, (1, 8)) * 3)
   d = t[0].duration
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0].format == 's8'
   assert t[0]._parent is t
   assert t[0].duration == d


### TEST OCTAVE ZERO ###

def test_octave_zero_01( ):
   '''Notes print correctly when pitch is in octave 0.'''
   t = Note(-37, (1, 4))
   assert t.format == 'b,,,4'


### ASSERTS ###

def test_assert_duration_is_notehead_assignable_01( ):
   raises(ValueError, Note, 0, (5, 8))
