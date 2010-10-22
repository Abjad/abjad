from abjad.components.Container import Container
from abjad.tools.chordtools.Cluster._ClusterFormatter import _ClusterFormatter


class Cluster(Container):

   def __init__(self, music = None, **kwargs):
      Container.__init__(self, music)
      self.is_parallel = False
      self._formatter = _ClusterFormatter(self)
      self._initialize_keyword_values(**kwargs)
   
   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._summary)
