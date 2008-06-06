from .. context.context import Context
from .. context.formatter import _ContextFormatter

class Voice(Context):

   def __init__(self, music = None):
      music = music or [ ]
      Context.__init__(self, music)
      self.invocation = 'Voice'
