from abjad.rational import Rational
from abjad.tools.construct.notes import notes as construct_notes


def run(count, written_duration = Rational(1, 8)):
   r'''Construct `count` notes on middle C with `written_duration`::

      abjad> construct.run(4)
      [Note(c', 8), Note(c', 8), Note(c', 8), Note(c', 8)]

   Allow nonassignable `written_duration`::

      abjad> voice = Voice(construct.run(2, (5, 16)))
      abjad> f(voice)
      \new Voice {
         c'4 ~
         c'16
         c'4 ~
         c'16
      }
   '''

   return construct_notes([0] * count, [written_duration])
