from abjad.note.note import Note
from abjad.helpers.diatonicize import diatonicize


def scale(count):
   result = Note(0, (1, 8)) * count
   diatonicize(result)
   return result
