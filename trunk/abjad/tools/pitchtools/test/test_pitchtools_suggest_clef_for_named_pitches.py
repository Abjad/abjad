from abjad import *


def test_pitchtools_suggest_clef_for_named_pitches_01( ):

   pitches = [10, 20, 30]
   pitches = [pitchtools.NamedPitch(x) for x in pitches]

   assert pitchtools.suggest_clef_for_named_pitches(pitches) == contexttools.ClefMark('treble')


def test_pitchtools_suggest_clef_for_named_pitches_02( ):

   pitches = [-10, -20, -30]
   pitches = [pitchtools.NamedPitch(x) for x in pitches]

   assert pitchtools.suggest_clef_for_named_pitches(pitches) == contexttools.ClefMark('bass')


def test_pitchtools_suggest_clef_for_named_pitches_03( ):

   pitches = [10, 20, -30]
   pitches = [pitchtools.NamedPitch(x) for x in pitches]

   assert pitchtools.suggest_clef_for_named_pitches(pitches) == contexttools.ClefMark('bass')


def test_pitchtools_suggest_clef_for_named_pitches_04( ):

   pitches = [-10, -20, 30]
   pitches = [pitchtools.NamedPitch(x) for x in pitches]

   assert pitchtools.suggest_clef_for_named_pitches(pitches) == contexttools.ClefMark('treble')


def test_pitchtools_suggest_clef_for_named_pitches_05( ):
   '''Works with arbitrary expression.'''

   staff = Staff(notetools.make_notes(range(-12, -6), [(1, 4)]))
   
   assert pitchtools.suggest_clef_for_named_pitches(staff) == contexttools.ClefMark('bass')
