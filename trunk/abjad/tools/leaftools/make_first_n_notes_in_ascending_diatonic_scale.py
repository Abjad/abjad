from abjad.note import Note
from abjad.rational import Rational
from abjad.tools import pitchtools
from abjad.tools.leaftools.make_notes import make_notes


def make_first_n_notes_in_ascending_diatonic_scale(count, written_duration = Rational(1, 8), key_signature = None):
   r'''Construct `count` notes with `written_duration`
   according to `key_signature`::

      abjad> macros.scale(4)
      [Note(c', 8), Note(d', 8), Note(e', 8), Note(f', 8)]

   Allow nonassignable `written_duration`::

      abjad> staff = Staff(macros.scale(2, (5, 16)))
      abjad> f(staff)
      \new Staff {
              c'4 ~
              c'16
              d'4 ~
              d'16
      }   

   .. versionadded:: 1.1.2
      Optional `key_signature` keyword parameter.

   .. versionchanged:: 1.1.2
      renamed ``construct.scale( )`` to
      ``macros.scale( )``.
   '''

   result = make_notes([0] * count, [written_duration])
   pitchtools.diatonicize(result, key_signature)
   return result
