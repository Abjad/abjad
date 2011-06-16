from abjad import *
import copy


def test_Note___copy___01( ):
   '''Copy note.
   '''

   note_1 = Note(12, (1, 4))
   note_2 = copy.copy(note_1)

   assert isinstance(note_1, Note)
   assert isinstance(note_2, Note)
   assert note_1.format == note_2.format
   assert note_1 is not note_2


def test_Note___copy___02( ):
   '''Copy note with LilyPond multiplier.
   '''

   note_1 = Note(12, (1, 4), (1, 2))
   note_2 = copy.copy(note_1)

   assert isinstance(note_1, Note)
   assert isinstance(note_2, Note)
   assert note_1.format == note_2.format
   assert note_1 is not note_2


def test_Note___copy___03( ):
   '''Copy note with LilyPond grob overrides and LilyPond context settings.
   '''

   note_1 = Note(12, (1, 4))
   note_1.override.staff.note_head.color = 'red'
   note_1.override.accidental.color = 'red'
   note_1.set.tuplet_full_length = True
   note_2 = copy.copy(note_1)

   assert isinstance(note_1, Note)
   assert isinstance(note_2, Note)
   assert note_1.format == note_2.format
   assert note_1 is not note_2
