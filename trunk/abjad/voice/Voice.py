from abjad.context import _Context


class Voice(_Context):
   '''*Abjad* model of a musical voice.'''

   def __init__(self, music = None):
      '''Initialize voice as type of musical context.'''
      _Context.__init__(self, music)
      self.context = 'Voice'
