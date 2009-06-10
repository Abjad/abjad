from abjad.note.note import Note
from abjad.rational.rational import Rational


def run(count, duration = Rational(1, 8)):
   '''Returns a list of notes with equal duration and same middle 
   C pitch.

   * *count*, the number of notes to create.
   * *duration*, a duration token indicating the duration of each note.\
      The default is 1/8.


   Examples:

   ::

      abjad> construct.run(4)
      [Note(c', 8), Note(c', 8), Note(c', 8), Note(c', 8)]

   ::

      abjad> construct.run(4, (1, 16))
      [Note(c', 16), Note(c', 16), Note(c', 16), Note(c', 16)]

   '''

   return Note(0, duration) * count
