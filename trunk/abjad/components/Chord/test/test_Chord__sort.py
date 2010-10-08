from abjad import *


def test_Chord__sort_01( ):
   '''Pitches manifestly different and sorted at initialization.'''
   t = Chord([pitchtools.NamedChromaticPitch('c', 4), pitchtools.NamedChromaticPitch('d', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].numbered_diatonic_pitch != t.pitches[1].numbered_diatonic_pitch
   assert t.pitches[0].numbered_chromatic_pitch != t.pitches[1].numbered_chromatic_pitch
   assert t.pitches[0] == pitchtools.NamedChromaticPitch('c', 4)
   assert t.pitches[1] == pitchtools.NamedChromaticPitch('d', 4)


def test_Chord__sort_02( ):
   '''Pitches manifestly different but NOT sorted at initialization.'''
   t = Chord([pitchtools.NamedChromaticPitch('d', 4), pitchtools.NamedChromaticPitch('c', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].numbered_diatonic_pitch != t.pitches[1].numbered_diatonic_pitch
   assert t.pitches[0].numbered_chromatic_pitch != t.pitches[1].numbered_chromatic_pitch
   assert t.pitches[0] == pitchtools.NamedChromaticPitch('c', 4)
   assert t.pitches[1] == pitchtools.NamedChromaticPitch('d', 4)


def test_Chord__sort_03( ):
   '''Pitches different only by accidentals but sorted at initialization.'''
   t = Chord([pitchtools.NamedChromaticPitch('c', 4), pitchtools.NamedChromaticPitch('cs', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].numbered_diatonic_pitch == t.pitches[1].numbered_diatonic_pitch
   assert t.pitches[0].numbered_chromatic_pitch != t.pitches[1].numbered_chromatic_pitch
   assert t.pitches[0] == pitchtools.NamedChromaticPitch('c', 4)
   assert t.pitches[1] == pitchtools.NamedChromaticPitch('cs', 4)
   

def test_Chord__sort_04( ):
   '''Pitches different only by accidentals and NOT sorted at initialization.'''
   t = Chord([pitchtools.NamedChromaticPitch('cs', 4), pitchtools.NamedChromaticPitch('c', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].numbered_diatonic_pitch == t.pitches[1].numbered_diatonic_pitch
   assert t.pitches[0].numbered_chromatic_pitch != t.pitches[1].numbered_chromatic_pitch
   assert t.pitches[0] == pitchtools.NamedChromaticPitch('c', 4)
   assert t.pitches[1] == pitchtools.NamedChromaticPitch('cs', 4)
   

def test_Chord__sort_05( ):
   '''Pitches enharmonically equivalent but sorted at initialization.'''
   t = Chord([pitchtools.NamedChromaticPitch('cs', 4), pitchtools.NamedChromaticPitch('df', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].numbered_diatonic_pitch != t.pitches[1].numbered_diatonic_pitch
   assert t.pitches[0].numbered_chromatic_pitch == t.pitches[1].numbered_chromatic_pitch
   assert t.pitches[0] == pitchtools.NamedChromaticPitch('cs', 4)
   assert t.pitches[1] == pitchtools.NamedChromaticPitch('df', 4)


def test_Chord__sort_06( ):
   '''Pitches enharmonically equivalent and NOT sorted in initialziation.'''
   t = Chord([pitchtools.NamedChromaticPitch('df', 4), pitchtools.NamedChromaticPitch('cs', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].numbered_diatonic_pitch != t.pitches[1].numbered_diatonic_pitch
   assert t.pitches[0].numbered_chromatic_pitch == t.pitches[1].numbered_chromatic_pitch
   assert t.pitches[0] == pitchtools.NamedChromaticPitch('cs', 4)
   assert t.pitches[1] == pitchtools.NamedChromaticPitch('df', 4)


def test_Chord__sort_07( ):
   '''Pitches typographically crossed but sorted at initialization.'''
   t = Chord([pitchtools.NamedChromaticPitch('css', 4), pitchtools.NamedChromaticPitch('dff', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].numbered_diatonic_pitch != t.pitches[1].numbered_diatonic_pitch
   assert t.pitches[0].numbered_chromatic_pitch != t.pitches[1].numbered_chromatic_pitch
   assert t.pitches[0] == pitchtools.NamedChromaticPitch('css', 4)
   assert t.pitches[1] == pitchtools.NamedChromaticPitch('dff', 4)


def test_Chord__sort_08( ):
   '''Pitches typographically crossed and NOT sorted at initialization.'''
   t = Chord([pitchtools.NamedChromaticPitch('dff', 4), pitchtools.NamedChromaticPitch('css', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].numbered_diatonic_pitch != t.pitches[1].numbered_diatonic_pitch
   assert t.pitches[0].numbered_chromatic_pitch != t.pitches[1].numbered_chromatic_pitch
   assert t.pitches[0] == pitchtools.NamedChromaticPitch('css', 4)
   assert t.pitches[1] == pitchtools.NamedChromaticPitch('dff', 4)
