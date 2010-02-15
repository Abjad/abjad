from abjad.note import Note
from abjad.rational import Rational
from abjad.tools import pitchtools


def scale(count, duration = Rational(1, 8), key_signature = None):
   '''Returns a list of notes with equal duration according to
   ascending pitches in `key_signature`.

   * `count`, the number of notes to create.
   * `duration`, a duration token indicating the duration of each note. \
      The default is 1/8.

   Examples::

      abjad> construct.scale(4)
      [Note(c', 8), Note(d', 8), Note(e', 8), Note(f', 8)]

   :: 

      abjad> construct.scale(4, (1, 16))
      [Note(c', 16), Note(d', 16), Note(e', 16), Note(f', 16)]

   .. versionadded:: 1.1.2
      Optional `key_signature` keyword parameter.
   '''

   result = Note(0, duration) * count
   pitchtools.diatonicize(result, key_signature)
   return result
