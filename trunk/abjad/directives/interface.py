from abjad.core.interface import _Interface
from abjad.comments.comments import _UserComments


class UserDirectivesInterface(_Interface, _UserComments):
   '''Interface to handle literal *LilyPond* directives that \
   are not yet modelled explicitly in *Abjad*.'''

   def __init__(self, component):
      '''Init as a subclass of the user comments interface.'''
      _Interface.__init__(self, component)
      _UserComments.__init__(self)
      self._left = [ ]

   ## PUBLIC ATTRIBUTES ##

   @apply
   def left( ):
      def fget(self):
         '''User directives to left of component.
         
         .. todo:: deprecated ``left`` formatting slot altogether.'''
         return self._left
      def fset(self, arg):
         assert arg is None
         self._left = [ ]
      return property(**locals( ))

   @property
   def locations(self):
      '''Format locations into which user may place directives.'''
      return ('before', 'opening', 'left', 'right', 'closing', 'after')
