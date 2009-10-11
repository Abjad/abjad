from abjad.core.interface import _Interface
from abjad.interfaces.comments.interface import CommentsInterface


class DirectivesInterface(_Interface, CommentsInterface):
   '''Interface to handle literal LilyPond directives that
   are not yet modelled explicitly in Abjad.'''

   def __init__(self, component):
      '''Init as a subclass of comments interface.
      '''

      _Interface.__init__(self, component)
      CommentsInterface.__init__(self)
