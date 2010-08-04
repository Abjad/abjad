from abjad.core import Rational
from abjad.tools.leaftools.make_notes import make_notes


def make_repeated_notes(count, written_duration = Rational(1, 8)):
   r'''Construct `count` notes on middle C with `written_duration`::

      abjad> leaftools.make_repeated_notes(4)
      [Note(c', 8), Note(c', 8), Note(c', 8), Note(c', 8)]

   Allow nonassignable `written_duration`::

      abjad> voice = Voice(leaftools.make_repeated_notes(2, (5, 16)))
      abjad> f(voice)
      \new Voice {
         c'4 ~
         c'16
         c'4 ~
         c'16
      }

   .. versionchanged:: 1.1.2
      renamed ``construct.run( )`` to
      ``leaftools.make_repeated_notes( )``.
   '''

   return make_notes([0] * count, [written_duration])
