from .. containers.container import Container
from formatter import _GraceFormatter


class Grace(Container):

   def __init__(self, music = [ ]):
      Container.__init__(self, music)
      self.formatter = _GraceFormatter(self)
      self._type = 'grace'
