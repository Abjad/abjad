from abjad.container.container import Container
from abjad.cluster.formatter import _ClusterFormatter
from abjad.cluster.interface import _ClusterInterface


class Cluster(Container):

   def __init__(self, music = None):
      Container.__init__(self, music)
      #self.brackets = 'curly'
      self.parallel = False
      self._formatter = _ClusterFormatter(self)
      self._cluster = _ClusterInterface(self)
   
   ## OVERLOADS ##

   def __repr__(self):
      return 'Cluster(%s)' % self._summary
   
   ## PUBLIC ATTRIBUTES ##

   @property
   def cluster(self):
      return self._cluster
