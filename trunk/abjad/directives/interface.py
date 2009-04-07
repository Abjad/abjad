from abjad.core.interface import _Interface
from abjad.comments.comments import _UserComments


class _UserDirectivesInterface(_Interface, _UserComments):

   def __init__(self, component):
      _Interface.__init__(self, component)
      _UserComments.__init__(self)
      self._left = [ ]

   ## PUBLIC ATTRIBUTES ##

   @apply
   def left( ):
      def fget(self):
         return self._left
      def fset(self, arg):
         assert arg is None
         self._left = [ ]
      return property(**locals( ))

   @property
   def locations(self):
      return ('before', 'opening', 'left', 'right', 'closing', 'after')
