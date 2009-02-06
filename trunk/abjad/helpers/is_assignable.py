from abjad.helpers.binary import _binary
from abjad.rational.rational import Rational


def _is_assignable(rational):
   '''Return True when 'rational' p/q is of a form
      acceptable for assignment as written duration
      to a note, rest, chord or skip, otherwise False.'''

   rational = Rational(rational)
   return (not rational._d & (rational._d - 1)) and \
      (0 < rational < 16) and \
      (not '01' in _binary(rational._n))
