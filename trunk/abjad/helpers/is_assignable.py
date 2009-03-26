from abjad.helpers.binary import _binary
from abjad.helpers.is_power_of_two import _is_power_of_two
from abjad.rational.rational import Rational


def is_assignable(rational):
   '''Return True when 'rational' p/q is of a form
      acceptable for assignment as written duration
      to a note, rest, chord or skip, otherwise False.'''

   rational = Rational(rational)
   return _is_power_of_two(rational._d) and \
      (0 < rational < 16) and \
      (not '01' in _binary(rational._n))
