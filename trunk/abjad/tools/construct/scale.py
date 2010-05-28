from abjad.note import Note
from abjad.rational import Rational
from abjad.tools import pitchtools
from abjad.tools.construct.notes import notes as construct_notes


def scale(count, written_duration = Rational(1, 8), key_signature = None):
   r'''Construct `count` notes with `written_duration`
   according to `key_signature`::

      abjad> construct.scale(4)
      [Note(c', 8), Note(d', 8), Note(e', 8), Note(f', 8)]

   Allow nonassignable `written_duration`::

      abjad> staff = Staff(construct.scale(2, (5, 16)))
      abjad> f(staff)
      \new Staff {
              c'4 ~
              c'16
              d'4 ~
              d'16
      }   

   .. versionadded:: 1.1.2
      Optional `key_signature` keyword parameter.
   '''

   result = construct_notes([0] * count, [written_duration])
   pitchtools.diatonicize(result, key_signature)
   return result
