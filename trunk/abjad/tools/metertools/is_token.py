from abjad.meter.meter import Meter
from abjad.rational.rational import Rational
from abjad.tools import durtools


def is_token(arg):
   '''Return True when arg has the form of an
      Abjad meter token, otherwise False.'''

   if isinstance(arg, Meter):
      return True
   elif isinstance(arg, Rational):
      return True
   elif durtools.is_pair(arg):
      return True
   else:
      return False
