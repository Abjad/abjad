from abjad.core.formatcontributor import _FormatContributor
from abjad.interfaces.interface.interface import _Interface
from abjad.tools import mathtools


class TremoloInterface(_Interface, _FormatContributor):
   '''Publish tremolo subdivision settings.
      Handle no LilyPond grob.'''

   def __init__(self, client):
      '''Bind to client and set subdivision to None.'''
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      self._subdivision = None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def subdivision( ):
      '''Read / write positive power-of-two tremolo subdivision.'''
      def fget(self):
         return self._subdivision
      def fset(self, arg):
         assert arg is None or mathtools.is_power_of_two(arg)
         self._subdivision = arg
      return property(**locals())
