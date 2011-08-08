from abjad.tools.componenttools._Component._ComponentDurationInterface import _ComponentDurationInterface
from abjad.exceptions import AssignabilityError
from abjad.exceptions import MissingTempoError
from abjad.interfaces._Interface import _Interface
from abjad.tools import durtools
import fractions


class _LeafDurationInterface(_ComponentDurationInterface):

   __slots__ = ('_multiplier', '_written', )

   def __init__(self, _client, duration_token):
      _ComponentDurationInterface.__init__(self, _client)
      #self.multiplier = None
      ## delete this line after migration
      self._multiplier = None
      #self.written = durtools.Duration(durtools.duration_token_to_duration_pair(duration_token))

   ## OVERLOADS ##

   def __str__(self):
      from abjad.tools import durtools
      #duration_string = durtools.assignable_rational_to_lilypond_duration_string(self.written)
      duration_string = durtools.assignable_rational_to_lilypond_duration_string(self._client.written_duration)
      #if self.multiplier is not None:
      #   return '%s * %s' % (duration_string, self._multiplier)
      if self._client.duration_multiplier is not None:
         return '%s * %s' % (duration_string, self._client.duration_multiplier)
      else:
         return duration_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _duration(self):
      return self.multiplied

   ## PUBLIC ATTRIBUTES ##

#   @property
#   def multiplied(self):
#      if self.written:
#         if self.multiplier is not None:
#            return self.written * self.multiplier
#         else:
#            return durtools.Duration(self.written)
#      else:
#         return None

#   @apply
#   def multiplier( ):
#      def fget(self):
#         return self._multiplier
#      def fset(self, expr):
#         if expr is None:
#            self._multiplier = None
#         else:
#            if isinstance(expr, fractions.Fraction):
#               rational = expr
#            elif isinstance(expr, (int, long)):
#               rational = fractions.Fraction(expr)
#            elif isinstance(expr, tuple):
#               rational = fractions.Fraction(*expr)
#            else:
#               raise TypeError('can not set duration multiplier: "%s".' % str(expr))
#            assert 0 <= rational
#            self._multiplier = rational
#      return property(**locals( ))

   @apply
   def preprolated( ):
      def fget(self):
         #return self.multiplied
         return self._client.multiplied_duration
      return property(**locals( ))

#   @property
#   def seconds(self):
#      from abjad.tools import contexttools
#      tempo = contexttools.get_effective_tempo(self._client)
#      if tempo is not None:
#         return self.prolated / tempo.duration / tempo.units_per_minute * 60
#      raise MissingTempoError

#   @apply
#   def written( ):
#      def fget(self):
#         return self._written
#      def fset(self, expr):
##         if isinstance(expr, Duration):
##            rational = expr
##         elif isinstance(expr, (int, long)):
##            rational = Duration(expr)
##         else:
##            raise ValueError('can not set written duration: "%s".' % str(expr))
#         rational = durtools.Duration(expr)
#         if not durtools.is_assignable_rational(rational):
#            raise AssignabilityError('not assignable duration: "%s".' % str(rational))
#         self._written = rational
#      return property(**locals( ))
