from abjad.core.formatcontributor import _FormatContributor
from abjad.core.interface import _Interface
from abjad.helpers.is_power_of_two import _is_power_of_two


class _TremoloInterface(_Interface, _FormatContributor):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      self._subdivision = None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def subdivision( ):
      def fget(self):
         return self._subdivision
      def fset(self, arg):
         assert arg is None or _is_power_of_two(arg)
         self._subdivision = arg
      return property(**locals())
