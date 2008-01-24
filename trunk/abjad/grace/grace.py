from .. containers.container import Container
from formatter import GraceFormatter


class Grace(Container):

   def __init__(self, music = [ ]):
      Container.__init__(self, music)
      self.formatter = GraceFormatter(self)
