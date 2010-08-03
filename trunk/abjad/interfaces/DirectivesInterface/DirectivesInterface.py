from abjad.interfaces.interface.interface import _Interface
from abjad.interfaces.comments.interface import CommentsInterface


class DirectivesInterface(_Interface, CommentsInterface):
   '''Interface to handle literal LilyPond directives that
   are not yet modelled explicitly in Abjad.'''

   def __init__(self, component):
      '''Init as a subclass of comments interface.'''
      _Interface.__init__(self, component)
      CommentsInterface.__init__(self)

   ## TODO: add a 'with' option for contexts. ##
   ##       Will probably need to subclass this interface for contexts. ##
