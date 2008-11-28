from abjad.core.formatcarrier import _FormatCarrier
from abjad.core.interface import _Interface


class _TremoloInterface(_Interface, _FormatCarrier):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatCarrier.__init__(self)
      self._subdivision = None

   ### PUBLIC ATTRIBUTES ###

   @property
   def body(self):
      if self.subdivision:
         return [':' + str(self.subdivision)]
      else:
         return [ ]

   @apply
   def subdivision( ):
      def fget(self):
         return self._subdivision
      def fset(self, expr):
         self._subdivision = expr
      return property(**locals())
