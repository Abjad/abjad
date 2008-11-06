#from .. context.context import Context
from .. context.context import _Context
from .. context.formatter import _ContextFormatter

#class Voice(Context):
class Voice(_Context):

   def __init__(self, music = None):
      music = music or [ ]
      #Context.__init__(self, music)
      _Context.__init__(self, music)
      self.invocation = 'Voice'
