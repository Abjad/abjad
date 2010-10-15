from abjad import *
import copy


def test_Chord___copy___01( ):
   '''Copy chord.
   '''

   chord_1 = Chord([3, 13, 17], (1, 4))
   chord_2 = copy.copy(chord_1)

   assert isinstance(chord_1, Chord)
   assert isinstance(chord_2, Chord)
   assert chord_1 == chord_2
   assert chord_1.format == chord_2.format
   assert chord_1 is not chord_2


def test_Chord___copy___02( ):
   '''Copy chord with LilyPond multiplier.
   '''

   chord_1 = Chord([3, 13, 17], (1, 4), (1, 2))
   chord_2 = copy.copy(chord_1)

   assert isinstance(chord_1, Chord)
   assert isinstance(chord_2, Chord)
   assert chord_1 == chord_2
   assert chord_1.format == chord_2.format
   assert chord_1 is not chord_2


def test_Chord___copy___03( ):
   '''Copy chord with LilyPond grob overrides and LilyPond context settings.
   '''

   chord_1 = Chord([3, 13, 17], (1, 4))
   chord_1.override.staff.note_head.color = 'red'
   chord_1.override.accidental.color = 'red'
   chord_1.set.tuplet_full_length = True
   chord_2 = copy.copy(chord_1)

   assert isinstance(chord_1, Chord)
   assert isinstance(chord_2, Chord)
   assert chord_1 == chord_2
   assert chord_1.format == chord_2.format
   assert chord_1 is not chord_2
