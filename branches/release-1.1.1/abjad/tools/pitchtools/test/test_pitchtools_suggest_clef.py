from abjad import *


def test_pitchtools_suggest_clef_01( ):

   pitches = [10, 20, 30]
   pitches = [Pitch(x) for x in pitches]

   assert pitchtools.suggest_clef(pitches) == Clef('treble')


def test_pitchtools_suggest_clef_02( ):

   pitches = [-10, -20, -30]
   pitches = [Pitch(x) for x in pitches]

   assert pitchtools.suggest_clef(pitches) == Clef('bass')


def test_pitchtools_suggest_clef_03( ):

   pitches = [10, 20, -30]
   pitches = [Pitch(x) for x in pitches]

   assert pitchtools.suggest_clef(pitches) == Clef('bass')


def test_pitchtools_suggest_clef_04( ):

   pitches = [-10, -20, 30]
   pitches = [Pitch(x) for x in pitches]

   assert pitchtools.suggest_clef(pitches) == Clef('treble')
