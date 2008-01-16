from .. context.context import Context
from .. context.formatter import ContextFormatter

class Voice(Context):

   def __init__(self, music = [ ]):
      Context.__init__(self, music)
      self.invocation = 'Voice'
