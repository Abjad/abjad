from abjad.component.duration import _ComponentDurationInterface
from abjad.interfaces.interface.interface import _Interface
from abjad.exceptions import AssignabilityError
from abjad.exceptions import UndefinedTempoError
from abjad.tools import durtools
from abjad.rational import Rational


class _LeafDurationInterface(_ComponentDurationInterface):

   def __init__(self, _client, duration_token):
      _ComponentDurationInterface.__init__(self, _client)
      self.multiplier = None
      self.written = Rational(*durtools.duration_token_to_reduced_duration_pair(duration_token))

   ## OVERLOADS ##

   def __str__(self):
      from abjad.tools import durtools
      duration_string = durtools.assignable_rational_to_lilypond_duration_string(self.written)
      if self.multiplier is not None:
         return '%s * %s' % (duration_string, self.multiplier)
      else:
         return duration_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _duration(self):
      return self.multiplied

   ## PUBLIC ATTRIBUTES ##

   @property
   def multiplied(self):
      if self.written:
         if self.multiplier:
            return self.written * self.multiplier
         else:
            return Rational(self.written)
      else:
         return None

   @apply
   def multiplier( ):
      def fget(self):
         return self._multiplier
      def fset(self, expr):
         if expr is None:
            self._multiplier = None
         else:
            if isinstance(expr, Rational):
               rational = expr
            elif isinstance(expr, (int, long)):
               rational = Rational(expr)
            else:
               raise ValueError('can not set duration multiplier')
            assert rational >= 0
            self._multiplier = rational
      return property(**locals( ))

   @apply
   def preprolated( ):
      def fget(self):
         return self.multiplied
      return property(**locals( ))

   @property
   def seconds(self):
      tempo = self._client.tempo.effective
      if tempo is not None:
         return self.prolated / tempo.duration / tempo.units_per_minute * 60
      raise UndefinedTempoError

   @apply
   def written( ):
      def fget(self):
         return self._written
      def fset(self, expr):
         if isinstance(expr, Rational):
            rational = expr
         elif isinstance(expr, (int, long)):
            rational = Rational(expr)
         else:
            raise ValueError('can not set written duration.')
         if not durtools.is_assignable_rational(rational):
            raise AssignabilityError('%s' % str(rational))
         self._written = rational
      return property(**locals( ))
