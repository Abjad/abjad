from abjad import *


def test_chordtools_divide_chord_by_diatonic_pitch_number_01( ):
   '''Chord split by diatonic pitch number only; empty bass.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.divide_chord_by_diatonic_pitch_number(t, pitchtools.NamedPitch('d', 4))
   assert isinstance(treble, Chord)
   assert treble == Chord([2, 3, 4], (1, 4))
   assert isinstance(bass, Rest)
   assert bass == Rest((1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass
   

def test_chordtools_divide_chord_by_diatonic_pitch_number_02( ):
   '''Chord split by diatonic pitch number only; one-note bass.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.divide_chord_by_diatonic_pitch_number(t, pitchtools.NamedPitch('e', 4))
   assert isinstance(treble, Chord)
   assert treble == Chord([3, 4], (1, 4))
   assert isinstance(bass, Note)
   assert bass == Note(2, (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass
   

def test_chordtools_divide_chord_by_diatonic_pitch_number_03( ):
   '''Chord split by diatonic pitch number is accidental agnostic.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble1, bass1 = chordtools.divide_chord_by_diatonic_pitch_number(t, pitchtools.NamedPitch('e', 4))
   treble2, bass2 = chordtools.divide_chord_by_diatonic_pitch_number(t, pitchtools.NamedPitch('ef', 4))
   assert treble1 == treble2
   assert bass1 == bass2


def test_chordtools_divide_chord_by_diatonic_pitch_number_04( ):
   '''Typographically crossed split by diatonic pitch number only.'''
   t = Chord([('d', 4), ('es', 4), ('ff', 4), ('g', 4)], (1, 4))
   treble, bass = chordtools.divide_chord_by_diatonic_pitch_number(t, pitchtools.NamedPitch('f', 4))
   assert isinstance(treble, Chord)
   assert treble == Chord([('ff', 4), ('g', 4)], (1, 4))
   assert isinstance(bass, Chord)
   assert bass == Chord([('d', 4), ('es', 4)], (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_divide_chord_by_diatonic_pitch_number_05( ):
   '''Spanned chord DOES NOT copy spanner to resultant split parts.'''
   staff = Staff(Chord([2, 4, 5], (1, 4)) * 3)
   spannertools.BeamSpanner(staff)
   t = staff[1]
   treble, bass = chordtools.divide_chord_by_diatonic_pitch_number(t, pitchtools.NamedPitch('e', 4))
   assert isinstance(treble, Chord)
   assert len(treble.spanners) == 0
   assert isinstance(bass, Note)
   assert len(bass.spanners) == 0
   assert t is not treble
   assert t is not bass
   assert treble is not bass
