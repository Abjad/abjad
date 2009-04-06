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
   def contributions(self):
      result = [ ]
      result.append(('before', tuple(self.before)))
      result.append(('opening', tuple(self.opening)))
      result.append(('left', tuple(self.left)))
      result.append(('right', tuple(self.right)))
      result.append(('closing', tuple(self.closing)))
      result.append(('after', tuple(self.after)))
      return tuple(result)

   ## PUBLIC METHODS ##

   def clear(self):
      '''Remove all user directives.'''
      _UserComments.clear(self)
      self.left = None
