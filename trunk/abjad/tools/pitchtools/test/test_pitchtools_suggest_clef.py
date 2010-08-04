from abjad import *


def test_pitchtools_suggest_clef_01( ):

   pitches = [10, 20, 30]
   pitches = [NamedPitch(x) for x in pitches]

   assert pitchtools.suggest_clef(pitches) == Clef('treble')


def test_pitchtools_suggest_clef_02( ):

   pitches = [-10, -20, -30]
   pitches = [NamedPitch(x) for x in pitches]

   assert pitchtools.suggest_clef(pitches) == Clef('bass')


def test_pitchtools_suggest_clef_03( ):

   pitches = [10, 20, -30]
   pitches = [NamedPitch(x) for x in pitches]

   assert pitchtools.suggest_clef(pitches) == Clef('bass')


def test_pitchtools_suggest_clef_04( ):

   pitches = [-10, -20, 30]
   pitches = [NamedPitch(x) for x in pitches]

   assert pitchtools.suggest_clef(pitches) == Clef('treble')


def test_pitchtools_suggest_clef_05( ):
   '''Works with arbitrary expression.'''

   staff = Staff(leaftools.make_notes(range(-12, -6), [(1, 4)]))
   
   assert pitchtools.suggest_clef(staff) == Clef('bass')
