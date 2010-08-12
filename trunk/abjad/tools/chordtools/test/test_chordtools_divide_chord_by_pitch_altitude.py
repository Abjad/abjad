from abjad import *


def test_chordtools_divide_chord_by_pitch_altitude_01( ):
   '''Chord split by altitude only; empty bass.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.divide_chord_by_pitch_altitude(t, pitchtools.NamedPitch('d', 4))
   assert isinstance(treble, Chord)
   assert treble.signature == ((('d', 4), ('ef', 4), ('e', 4)), (1, 4))
   assert isinstance(bass, Rest)
   assert bass.signature == (( ), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass
   

def test_chordtools_divide_chord_by_pitch_altitude_02( ):
   '''Chord split by altitude only; one-note bass.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.divide_chord_by_pitch_altitude(t, pitchtools.NamedPitch('e', 4))
   assert isinstance(treble, Chord)
   assert treble.signature == ((('ef', 4), ('e', 4)), (1, 4))
   assert isinstance(bass, Note)
   assert bass.signature == ((('d', 4), ), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass
   

def test_chordtools_divide_chord_by_pitch_altitude_03( ):
   '''Chord split by altitude is accidental agnostic.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble1, bass1 = chordtools.divide_chord_by_pitch_altitude(t, pitchtools.NamedPitch('e', 4))
   treble2, bass2 = chordtools.divide_chord_by_pitch_altitude(t, pitchtools.NamedPitch('ef', 4))
   assert treble1.signature == treble2.signature
   assert bass1.signature == bass2.signature


def test_chordtools_divide_chord_by_pitch_altitude_04( ):
   '''Typographically crossed split by altitude only.'''
   t = Chord([('d', 4), ('es', 4), ('ff', 4), ('g', 4)], (1, 4))
   treble, bass = chordtools.divide_chord_by_pitch_altitude(t, pitchtools.NamedPitch('f', 4))
   assert isinstance(treble, Chord)
   assert treble.signature == ((('ff', 4), ('g', 4)), (1, 4))
   assert isinstance(bass, Chord)
   assert bass.signature == ((('d', 4), ('es', 4)), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_divide_chord_by_pitch_altitude_05( ):
   '''Spanned chord DOES NOT copy spanner to resultant split parts.'''
   staff = Staff(Chord([2, 4, 5], (1, 4)) * 3)
   BeamSpanner(staff)
   t = staff[1]
   treble, bass = chordtools.divide_chord_by_pitch_altitude(t, pitchtools.NamedPitch('e', 4))
   assert isinstance(treble, Chord)
   assert len(treble.spanners.attached) == 0
   assert isinstance(bass, Note)
   assert len(bass.spanners.attached) == 0
   assert t is not treble
   assert t is not bass
   assert treble is not bass
