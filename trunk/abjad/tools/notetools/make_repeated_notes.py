from abjad.core import Fraction
from abjad.tools.notetools.make_notes import make_notes


def make_repeated_notes(count, written_duration = Fraction(1, 8)):
   r'''Construct `count` notes on middle C with `written_duration`::

      abjad> notetools.make_repeated_notes(4)
      [Note(c', 8), Note(c', 8), Note(c', 8), Note(c', 8)]

   Allow nonassignable `written_duration`::

      abjad> voice = Voice(notetools.make_repeated_notes(2, (5, 16)))
      abjad> f(voice)
      \new Voice {
         c'4 ~
         c'16
         c'4 ~
         c'16
      }

   .. versionchanged:: 1.1.2
      renamed ``construct.run( )`` to
      ``notetools.make_repeated_notes( )``.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.make_repeated_notes( )`` to
      ``notetools.make_repeated_notes( )``.
   '''

   return make_notes([0] * count, [written_duration])
