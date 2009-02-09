from abjad.note.note import Note
from abjad.rational.rational import Rational


def run(count, duration = Rational(1, 8)):
   return Note(0, duration) * count
