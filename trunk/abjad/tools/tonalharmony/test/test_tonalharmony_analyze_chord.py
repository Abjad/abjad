from abjad import *


def test_tonalharmony_analyze_chord_01( ):
   '''The three inversions of a C major triad.'''

   chord_class = tonalharmony.analyze_chord(Chord([0, 4, 7], (1, 4)))
   assert chord_class == tonalharmony.ChordClass('c', 'major', 'triad', 'root')

   chord_class = tonalharmony.analyze_chord(Chord([4, 7, 12], (1, 4)))
   assert chord_class == tonalharmony.ChordClass('c', 'major', 'triad', 1)

   chord_class = tonalharmony.analyze_chord(Chord([7, 12, 16], (1, 4)))
   assert chord_class == tonalharmony.ChordClass('c', 'major', 'triad', 2)


def test_tonalharmony_analyze_chord_02( ):
   '''The four inversions of a C dominant seventh chord.'''

   chord_class = tonalharmony.analyze_chord(Chord([0, 4, 7, 10], (1, 4)))
   assert chord_class == tonalharmony.ChordClass('c', 'dominant', 7, 'root')

   chord_class = tonalharmony.analyze_chord(Chord([4, 7, 10, 12], (1, 4)))
   assert chord_class == tonalharmony.ChordClass('c', 'dominant', 7, 1)

   chord_class = tonalharmony.analyze_chord(Chord([7, 10, 12, 16], (1, 4)))
   assert chord_class == tonalharmony.ChordClass('c', 'dominant', 7, 2)

   chord_class = tonalharmony.analyze_chord(Chord([10, 12, 16, 19], (1, 4)))
   assert chord_class == tonalharmony.ChordClass('c', 'dominant', 7, 3)


def test_tonalharmony_analyze_chord_03( ):
   '''The five inversions of a C dominant ninth chord.'''

   chord_class = tonalharmony.analyze_chord(Chord([0, 4, 7, 10, 14], (1, 4)))
   assert chord_class == tonalharmony.ChordClass('c', 'dominant', 9, 'root')

   chord_class = tonalharmony.analyze_chord(Chord([4, 7, 10, 12, 14], (1, 4)))
   assert chord_class == tonalharmony.ChordClass('c', 'dominant', 9, 1)

   chord_class = tonalharmony.analyze_chord(Chord([7, 10, 12, 14, 16], (1, 4)))
   assert chord_class == tonalharmony.ChordClass('c', 'dominant', 9, 2)

   chord_class = tonalharmony.analyze_chord(Chord([10, 12, 14, 16, 19], (1, 4)))
   assert chord_class == tonalharmony.ChordClass('c', 'dominant', 9, 3)

   chord_class = tonalharmony.analyze_chord(Chord([2, 10, 12, 16, 19], (1, 4)))
   assert chord_class == tonalharmony.ChordClass('c', 'dominant', 9, 4)
