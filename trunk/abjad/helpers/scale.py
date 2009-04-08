from abjad.tools import pitches
from abjad.note.note import Note
from abjad.rational.rational import Rational


def scale(count, duration = Rational(1, 8)):
   result = Note(0, duration) * count
   pitches.diatonicize(result)
   return result
