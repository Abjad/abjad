from abjad import *


def test_tonalharmony_analyze_incomplete_chord_01( ):

   cc = tonalharmony.analyze_incomplete_chord(Chord(['g', 'b'], (1, 4)))
   assert cc == tonalharmony.ChordClass('g', 'major', 'triad', 'root')


def test_tonalharmony_analyze_incomplete_chord_02( ):

   cc = tonalharmony.analyze_incomplete_chord(Chord(['fs', 'g', 'b'], (1, 4)))
   assert cc == tonalharmony.ChordClass('g', 'dominant', 'seventh', 2)
